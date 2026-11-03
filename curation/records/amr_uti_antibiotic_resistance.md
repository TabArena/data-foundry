---
unique_name: amr_uti_antibiotic_resistance
name: 'AMR-UTI: Antimicrobial Resistance in Urinary Tract Infections'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2020'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.13026/hdza-eh80
- https://doi.org/10.1126/scitranslmed.aay5067
- https://physionet.org/content/antimicrobial-resistance-uti/1.0.0/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: urine specimens of about 80,000 patients at two Boston hospitals (2007-2016) with resistance to four first-line antibiotics, EHR features known at the visit and a published split by year; the empiric-antibiotic choice is the decision the source built it for.
- Source: Oberst, Boominathan, Zhou, Kanjilal and Sontag, "AMR-UTI: Antimicrobial Resistance in Urinary Tract Infections" v1.0.0, PhysioNet, 2020-11-04 (doi 10.13026/hdza-eh80), a de-identified version of the data of Kanjilal et al. 2020, "A decision algorithm to promote outpatient antimicrobial stewardship for uncomplicated urinary tract infection", Sci Transl Med 12(568):eaay5067. As published: `all_uti_features.csv`, `all_uti_resist_labels.csv` and `all_prescriptions.csv` with a data dictionary; "over 80,000 patients" at Massachusetts General Hospital and Brigham & Women's Hospital, 55,078 training patients ("All training specimens are in the years 2007-2013") and 26,807 test patients ("All test specimens are in the years 2014-2016"); an `uncomplicated` flag marks the paper's cohort (10,053 + 3,629 patients, 11,865 + 3,941 specimens). Labels: non-susceptibility to nitrofurantoin, TMP-SMX, ciprofloxacin and levofloxacin by 2017 CLSI breakpoints ("We treat both intermediate and resistant phenotypes as resistant"). Features: demographics, prior resistance and prior antibiotic exposure over several windows, prior organisms, Elixhauser comorbidities, department, colonization pressure, nursing-home visits, other infection sites, prior procedures. Prescriptions only for uncomplicated specimens.
- Use case: a clinician treating an uncomplicated UTI, at the visit and before the culture result, picks the narrowest antibiotic the infection is likely susceptible to (the algorithm "chose the treatment of the narrowest spectrum among those that were susceptible"; second-line use 11.0% against the clinicians' 33.6%); fit direct. Regime temporal by the source's year split (SPLIT-6, SPLIT-19), with patients holding several specimens inside (SPLIT-13).
- Siblings and duplicates: no record of this source. `ed_uti_urine_culture_prediction` (culture positivity in the emergency department), `southern_denmark_hospital_uti` and `driams_antimicrobial_resistance` (resistance from MALDI-TOF spectra) are other sources or tasks (PROV-7). External collections: none found beyond PhysioNet; the same group used it for treatment-policy learning (Boominathan et al. 2020, KDD).
- Better data: from the curator's Zotero collection (item 80); no further search this round.
- Papers and pages: Kanjilal et al. 2020 (the task; PMC9527766); the PhysioNet page.
- Metric: Kanjilal 2020 scores each antibiotic's model by AUROC on the test years (Table 2: 0.56 nitrofurantoin, 0.59 TMP-SMX, 0.64 ciprofloxacin and levofloxacin; "AUROC and 95% CI calculated using 1000 bootstrapped samples taken from the test set"), and the policy by the rates of inappropriate therapy and second-line use, with thresholds tuned over "11 false negative rates" to stay under "a mean second line antibiotic usage rate of 10%": a policy over four models, not one task's metric. Per antibiotic, `roc_auc`, the source's discrimination metric and the fallback (MET-5, MET-8); inputs none.
- Risks for /add-dataset: four targets, so one antibiotic per dataset or the curator picks one (CLEAN-18); the cohort (all specimens or the uncomplicated ones the paper used); the feature windows must close before the specimen date (check, LEAK); credentialed access (PhysioNet Credentialed Health Data License 1.5.0, CITI training; no criterion, EV-4, but a build needs an approved account); a weak signal (AUROC 0.56 to 0.64) is no argument against it (TP-2).
- Priority: gap 0 (medical & healthcare, binary and temporal are not thin), use case +, source +, shape + (about 80,000 patients, many engineered features, temporal), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 80: "PhysioNet".
- as published: urine specimens of 81,885 patients (55,078 train 2007-2013, 26,807 test 2014-2016) at MGH and BWH; one feature table (prior resistance, prior antibiotics, comorbidities, procedures, demographics ...; target: resistance to nitrofurantoin, TMP-SMX, ciprofloxacin and levofloxacin (four binary labels); access: registration.
- Why: Clear target with a decision at a fixed prediction point, a published temporal train/test split, and a single feature table.
- Adds: Antimicrobial stewardship with a temporal split; no such record. Caveat: credentialed PhysioNet licence (no redistribution).
