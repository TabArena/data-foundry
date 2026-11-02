---
unique_name: skull_bone_molecular_age
name: 'Forensic age from skull bone: DNA methylation, D-aspartic acid, pentosidine'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
original_source: Other
year: '2024'
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1007/s00414-024-03314-z
- https://europepmc.org/article/PMC/PMC11732915
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 190 deceased individuals with DNA methylation at six CpG sites, D-aspartic acid and pentosidine measured in skull bone, and chronological age as the target, from a forensic study with an open per-sample table; a real task, but tiny.
- Source: Becker, Bühren, Schmelzer, Reckert, Eickhoff, Ritz, Naue, "Molecular age prediction using skull bone samples from individuals with and without signs of decomposition: a multivariate approach combining analysis of posttranslational protein modifications and DNA methylation", Int J Legal Med (2024), doi 10.1007/s00414-024-03314-z, PMC11732915, CC BY 4.0 (read through Europe PMC: Abstract, Methods; a correction of 6 August 2026 was not read). As published: Supplementary Table S1A (`414_2024_3314_MOESM1_ESM.xlsx`, previewed): 190 rows x 17 columns: No., dataset (1-3), decomposition scores for head, trunk and extremities and a total d-score, age, sex, DNAm % at RPA2_3, ZYG11A_18, PDE4C_17, TRIM59_7, ELOVL2_8 and KLF14_3, D-Asp, pentosidine ("-" where missing) and the ridge-regression set. Dataset 1 trains (the paper's models use its 86 individuals aged 18 or more; the table also holds children), dataset 2 is an independent test set without decomposition (n = 44), dataset 3 decomposed bodies (n = 48).
- Use case: a forensic pathologist estimates the age at death of an unidentified body from a skull sample, to narrow the search among missing persons ("can provide important information in case of unidentified bodies", Abstract). Fit direct. Regime IID over individuals; the paper's split by collection set is a claim to check (SPLIT-5), and decomposition is a covariate (the d-score) rather than a group.
- Siblings and duplicates: no record of molecular or skeletal age estimation (grep: methylation, forensic, skull, pentosidine); `nhanes_age_prediction` predicts age from health-survey data, another task. External collections: none known.
- Better data: from the curator's Zotero collection (item 126); no further search this round.
- Papers and pages: the paper; on the test set MAE/RMSE 5.5/6.6 years (DNAm), 7.7/9.3 (pentosidine), 11.7/14.6 (D-Asp), and 7.4-11.8 MAE on decomposed bodies (Abstract).
- Metric: MAE and RMSE reported side by side (Abstract, Results), neither named as the criterion, so the fallback `rmse` in years (MET-5, MET-8); inputs none.
- Risks for /add-dataset: about 38 individuals per test fold with five folds (`Tiny Data`); the ridge-regression set column and the dataset number are bookkeeping, never features; pentosidine and D-Asp missing for part of the rows; minors in the table but outside the paper's models (decide the population, USE-5); sex and the decomposition scores are known when the sample is taken.
- Priority: gap 0 (medical and regression covered), use case + (the paper names the identification case), source + (a peer-reviewed paper with the per-sample table), shape 0 (190 individuals, about 10 features), risk - (tiny, protein markers partly missing, sets of different condition).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 126: "Molecular age prediction using skull bone samples from individuals with and without ...".
- as published: deceased individuals, 190 rows x ~12 columns (6 CpG DNAm %, D-Asp, pentosidine, sex, decomposition scores, set membership); target: chronological age at death (regression); access: open.
- Why: real measurements, open supplement, a published train / test / decomposed split
- Adds: a forensic regression task; tiny (likely Too Small), the decomposed set gives a shift test
