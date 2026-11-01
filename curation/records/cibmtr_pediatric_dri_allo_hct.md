---
unique_name: cibmtr_pediatric_dri_allo_hct
name: 'CIBMTR publication analysis dataset P-5383: A validated pediatric disease risk index for allogeneic hematopoietic cell transplantation (Qayed et ...'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2021'
domain: medical & healthcare
original_data_state: One Table
source_links:
- https://doi.org/10.1182/blood.2020009342
- https://cibmtr.org/CIBMTR/Resources/Publicly-Available-Datasets
- https://cibmtr.org/ReferenceCenter/PubList/PubDsDownload/Documents/P-5383.zip
- https://cibmtr.org/ReferenceCenter/PubList/PubDsDownload/Documents/DataDictionaryFiles/P-5383/PC19-01---data-dictionary.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 2,569 children with AML or ALL after allogeneic transplant at 84 centres, the registry's public analysis file for a validated prognostic index. The target is a censored survival time, so the task needs a fixed horizon.
- Source: Qayed et al., "A validated pediatric disease risk index for allogeneic hematopoietic cell transplantation", Blood 137(7):983 (2021) (https://doi.org/10.1182/blood.2020009342, PMID 33206937; the abstract was read on Europe PMC, the full text could not be reached). The file is CIBMTR publication analysis dataset P-5383 (study PC19-01). The zip, previewed 2026-10-31, holds a SAS file `pc19_01.sas7bdat` of 2021-07-09, the data dictionary and the terms of use. As published: 2,569 rows x 22 columns. Inputs: de-identified patient and centre ids (84 centres), sex, age, disease (AML 1,224, ALL 1,345), T/B lineage, cytogenetics, disease and MRD status at transplant, KPS, HCT-CI, CMV, conditioning, donor and HLA group, GVHD prophylaxis, a 2-level year group and the time from diagnosis to transplant. The paper's columns: the risk group `final` and the training/validation flag `selection`. Outcomes: `dead`/`intxsurv` (overall survival, 953 deaths) and `dfs`/`intxrel` (relapse or death). The dictionary's names differ in places: it lists `Score` and `inreltx`, which the file lacks, and `condint` for the file's `condgrp`; the file's `yeargp` is not in it.
- Use case: the transplant physician before transplant. The index "can be used to facilitate prognostication and stratification of children with AML and ALL for allogeneic transplantation" (abstract). Fit direct for death, or leukemia-free survival, within a horizon from the pre-transplant features. Regime: IID over patients, since the file has no transplant date beyond a 2-level year group and so allows no temporal split; or grouped by centre for a new centre. The curator decides (SPLIT-3).
- Siblings and duplicates: `bone_marrow_transplant_children` (`TBD -> 2nd Tier`; UCI, 187 children of one Wroclaw centre; "survival task ... scientific discovery"). There is no other CIBMTR record. The Kaggle competition "CIBMTR - Equity in post-HCT Survival Predictions" used synthetic data and has no record (not checked here). External collections: none found.
- Better data: found as better data for `bone_marrow_transplant_children` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Blood paper; CIBMTR's listing of publicly available datasets ("The CIBMTR makes its publication analysis datasets freely available to the public for secondary analysis").
- Metric: none found as a prediction metric. The abstract reports 5-year leukemia-free and overall survival by risk group with log-rank P values, a stratification rather than a scored prediction; the full text was not read for a C-index. So the fallback `roc_auc` on a fixed-horizon binary target (MET-5, MET-8). Inputs none.
- Risks for /add-dataset: censoring. In the preview, 683 patients are censored alive before 36 months, against 906 deaths by then, so a fixed horizon drops or mislabels them; choose the horizon (survivors have a median follow-up of 38 months). `final` is the paper's index, fit on the training half: a supervised score, so drop it (LEAK-27 if kept). `selection` is the paper's split (SPLIT-5). `dfs`, `intxrel` and the survival time are outcomes (LEAK). Code 99 means missing (CLEAN). `pseudocn` is a group, not a feature.
- Priority: gap 0 (medical and binary not thin), use case + (the paper names prognostication and stratification), source + (registry paper and dictionary), shape + (2,569 patients, about 15 mixed features, 84 centres), risk - (censored target, a fitted index in the file).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `bone_marrow_transplant_children`.
- as published: Patients: 2,569 children aged <18 with AML (1,224) or ALL (1,345) after allogeneic HCT, registry-reported, transplants from 2008 (start year on the CIBMTR listing); one row per patient, columns per ...; target: Overall survival / leukemia-free survival after transplant (time and event; 5-year OS 33-80% by risk group); access: open (direct download under the CIBMTR terms and conditions linked on the listing page).
- Why: Same task as the UCI set (survival of children after allogeneic HCT for hematologic disease, from patient, disease, donor and graft features known before transplant), measured in a multi-center registry instead of one Wroclaw center; the paper itself is a prognostic-model study
- Adds: About 14 times the patients (2,569 vs 187), many centers, a later era (2008 on), a prognostic use case stated by the authors; the record's 'scientific discovery' doubt does not apply. Caveat: two diseases (AML/ALL) only, and the public file may hold derived/categorized variables. CIBMTR lists about 160 such per-paper ...
