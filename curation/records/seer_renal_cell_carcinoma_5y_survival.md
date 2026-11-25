---
unique_name: seer_renal_cell_carcinoma_5y_survival
name: 'SEER renal cell carcinoma: 5-year overall survival'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Dated Event Log
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- 'Features: Revised Later'
- 'Target: Fixed Delay'
original_source: GOV Website
collection_period: 2000-2022
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://seer.cancer.gov/
- https://doi.org/10.1186/s12911-026-03654-3
- https://seer.cancer.gov/data/access.html
- https://seer.cancer.gov/data-software/documentation/seerstat/nov2025/seerstat-variable-dictionary-nov2025.pdf
- https://github.com/KatherLab/tabpfnbenchmark
- https://doi.org/10.21037/tau-23-319
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 2: five-year overall survival of kidney cancer in the NCI SEER registries (192,912 RCC patients of 2004-2015 in the paper it reproduces), a large documented prognosis task with a temporal split by year of diagnosis; Shaktah's label keeps a recent patient only if they died, and the use case is named only loosely.
- Source: National Cancer Institute, SEER Program, "Incidence - SEER Research Data, 17 Registries, Nov 2024 Sub (2000-2022)", "Site recode ICD-O-3/WHO 2008 = Kidney and Renal Pelvis" (Shaktah et al. 2026, Methods, "Datasets"; the site recode also holds renal pelvis urothelial carcinoma and Wilms tumour, and no histology filter is named). SEER Research Data is per person through SEER*Stat after acknowledging the SEER Research Data Use Agreement ("Each person who will access the data must submit a separate request", seer.cancer.gov/data/access.html). The agreement (November 2025 submission) says in clause 10 "Authorized User will not release, nor permit others to release, the Data to any other person", and its clause 19 ("Permitted Use of AI/ML Tools") allows approved users to "develop or validate analytical and generative AI models using the Data" within an approved request, but "may not share the model, including model parameters, except with collaborators who are also Approved Users" and may not use the data with any tool "that transmits data to an external provider": a release-checklist item, no criterion (EV-4), but no row of it can ship and every user must extract it themselves. As published: case listings, one row per tumour (year of diagnosis, age, sex, race, marital status, laterality, histology, grade, tumour size, T/N/M and stage, first-course surgery, radiation, chemotherapy, survival months, vital status, cause of death). The target in Shaktah's code (`SEER_RCC/TabPFN_SEER-RCC_CPU.py`): `np.where(df2["Survival months"] >= 60, 1, np.where(df2["Vital status recode (study cutoff used)"].astype(str).isin(["Dead"]), 0, np.nan))`, the same as for osteosarcoma; "Year of diagnosis" is kept as a feature.
- Use case: the paper it reproduces, Jiang, Chen, Chen, Wang, Han, Wen, "Machine learning algorithms being an auxiliary tool to predict the overall survival of patients with renal cell carcinoma using the SEER database", Transl Androl Urol 13(1):53-63 (2024), doi 10.21037/tau-23-319, read from the journal's HTML: RCC (ICD-O C64) diagnosed 2004-2015, 192,912 patients; "Our outcome of interest was the 5-year OS outcome"; four analysis groups (complete cases 92,475; with five-year survival 55,334; imputed 120,202 and 71,710); features race, sex, age, marital status, tumour location and size, histology, grade, TNM stage and surgery; the authors frame ML as an auxiliary tool for individualised postoperative management. Actor: a urologist or oncologist after nephrectomy planning follow-up and adjuvant therapy; fit approximate (overall, not cancer-specific, survival; no decision tied to the threshold). Collection: samples over time dated by year of diagnosis; target after a fixed 60-month window; a patient can hold two kidney tumours (bilateral); cases resubmitted with recodes; type Dated Event Log (SPLIT-34 rule 3).
- Split: leaf [L-ORDER.windows] (Temporal · windows on the time key) because [LOG.meets] later patients, [ORDER.order] year of diagnosis, [ORDER.windows] about 20 diagnosis years of thousands of cases each; gap five years (an outcome window still open: train only on diagnoses whose 60 months closed before the window). Open: the window length and refit cadence (one diagnosis year proposed, SPLIT-12); whether to cap rows (Shaktah sampled to 100,000).
- Siblings and duplicates: `seer_breast_cancer_5y_survival` (`TBD -> Yes`, 3: the same registry, five-year breast-cancer-specific death), `seer_breast_cancer_survival` (`TBD -> 2nd Tier`, 2: a 4,024-row DataPort cut of it, a PROV-6 version of the former), `seer_primary_site_from_metastases` (`TBD -> Yes`, 3: another task on the same registry, PROV-7), `fosp_cancer_registry_survival` (`TBD -> Yes`, 2: São Paulo registry, survival by site, which left "one dataset per cancer site or all sites with the topography as a feature" open). The siblings' precedent is one record per task on SEER (PROV-7: distinct cohorts and targets), not one SEER record. Same task type as `seer_breast_cancer_5y_survival` and `seer_osteosarcoma_survival` on disjoint patients and organ-specific features, so not a duplicate (PROV-7); the curator decides how many SEER five-year survival tasks enter. External collections: Shaktah et al. 2026 benchmark (not in our vocabulary).
- Better data: none from another source (data scout, 2026-11-25: no public row-level registry beyond SEER; NCDB and the English, Taiwanese and NPCR survival files are restricted). Newer versions of this source (PROV-6): SEER Research Data, 17 Registries, Nov 2025 submission (diagnoses 2000-2023, released April 2026); the 21-registry Limited-Field file is wider (about 1.7x the tumours) but drops AJCC TNM, the radiation recode and marital status, and has survival fields only in its SEER 21 (excl. IL) variant.
- Papers and pages: Shaktah et al. 2026 (AUROC LightGBM 0.864, LR 0.806, TabPFN 0.861; 70/30 random split, sampled to 100,000); Jiang et al. 2024 (XGBoost AUC 0.670 on complete cases, 0.818-0.848 in the groups restricted to "survival ≥5 years", which as summarised would leave no deaths; not settled from the HTML, to reread).
- Metric: Jiang et al. report AUC, C-index, calibration curves and Brier scores, AUC first in the abstract; Shaktah AUROC. One of several, so the fallback `roc_auc` (MET-1, MET-5, MET-8); inputs none.
- Risks for /add-dataset: restrict to diagnoses with five years of potential follow-up (to 2017 in the Nov 2024 submission, 2018 in Nov 2025), or the recent years hold only deaths and the kept year of diagnosis becomes a shortcut (SPLIT-9, LEAK, `Class-dependent Recording`); survival months, vital status and cause-of-death columns go (LEAK); the site recode mixes RCC with renal pelvis urothelial carcinoma and paediatric Wilms tumour: restrict to C64 and RCC histologies as in Jiang et al., to decide (USE-5); surgery, radiation and chemotherapy set the prediction point after treatment planning (USE-3); staging editions change over the years (AJCC 6th, 7th, EOD 2018), so a stage built across them is to harmonise (CLEAN); one tumour per patient. Release: the Research 17-registry Nov 2025 submission (2000-2023) is the newest; in the 21-registry Limited-Field database survival and vital status are only in the "SEER 21 (excl IL)" variant and AJCC TNM is absent (variable dictionary, Nov 2025). The agreement bars shipping rows (above).
- Priority: gap 0 (medical, binary, temporal not thin), use case 0 (auxiliary tool, no decision named), source + (NCI SEER, a paper), shape + (tens of thousands of cases, mixed types, many years), risk - (censoring shortcut through the year; cohort to define).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.
