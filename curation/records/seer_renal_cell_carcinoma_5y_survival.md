---
unique_name: seer_renal_cell_carcinoma_5y_survival
name: 'SEER renal cell carcinoma: 5-year overall survival'
checked_by:
- Andrej
suggestion: 'Yes'
priority: 2
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

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

CC (2026-11-25, Andrej): accepted for adding in the screening review (issue 2 A (after first-course treatment); issue 1 (cohort) open).

CC (2026-11-25, Andrej): kidney cancer cohort settled in the screening review (issue 1 A, C64 with RCC histologies, as liver cancer issue 1).

## Review

**Outcome:** not added; screened `TBD -> Yes`, priority 2. Five-year overall survival of renal cell carcinoma in SEER (192,912 patients of 2004-2015 in Jiang et al. 2024); the cohort is cut where five years of follow-up are complete.

**Main points:** RCC only or the whole kidney site recode (issue 1); prediction point before or after treatment (issue 2).

**Issues for Andrej:**

1. **RCC only, or the whole kidney and renal pelvis site recode?**

   * **Problem:**
     - Shaktah's extract takes Site recode "Kidney and Renal Pelvis", which also holds renal pelvis urothelial carcinoma and paediatric Wilms tumour; the source paper (Jiang and colleagues) takes C64 with RCC histologies[^use5].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | C64 with RCC histologies (implemented) | as Jiang et al. | the source task; one disease | fewer rows |
     | B | The whole site recode | histology as a feature | more rows | three diseases in one label |

   * **Recommendation:** A. **Decision:** A or B?

   **Andrej (2026-11-25, change):** Option B: The whole site recode.

   **Consistency check (AI, 2026-11-25):** B takes Shaktah's whole site recode here, while liver cancer issue 1 of this batch took the source paper's single-histology cohort; what sets kidney cancer apart?

   * **Problem:**
     - The liver option you set aside and the kidney option you chose are both Shaktah's unfiltered extract, and both put several cancers into one label[^cc1].
     - The source paper (Jiang and colleagues) restricts to C64 with RCC histologies; Wilms tumour is a childhood cancer with another oncologist and other treatment.
     - The São Paulo registry pools all sites (your issue 1 A there), but there the source paper pools them too.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep B as a recorded exception | whole site recode, histology a feature; the fact written down: the liver extract was also set aside for its label that counts unknown as no | more rows; like the São Paulo call | Wilms tumour keeps another actor; the source task set aside |
     | b | Take A, like liver cancer | C64 with RCC histologies | consistent with liver cancer and the source paper | fewer rows, still tens of thousands |
     | c | Drop only Wilms tumour | adults' kidney and renal pelvis cancers, histology a feature | removes the clearest change of actor | our own cohort, in no source |
     | d | Pool for every SEER record | reopen liver issue 1 to the pooled cohort with a fixed label | one rule for the SEER records | goes against the source task |

   * **Recommendation:** b; a if the pooled table is what you want, with its fact written as the exception. The answer also settles osteosarcoma issue 1. **Decision:** a, b, c or d?

   **Andrej (2026-11-25, change):** Reply (b): Take A, like liver cancer.

   **Resolved (2026-11-25, Andrej):** A: C64 with RCC histologies, as the source paper and as liver cancer issue 1; the consistency check is answered with (b), so no exception is written.

   [^cc1]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it. Check how the source built its label before accepting it.

   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it. Check how the source built its label before accepting it.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.

2. **Prediction point: after treatment planning, or at diagnosis?**

   * **Problem:**
     - The source paper (Jiang and colleagues) frames the model for postoperative management and use surgery as a feature; radiation and chemotherapy are "yes" against "no/unknown" in SEER[^use3].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | After first-course treatment (implemented) | surgery, radiation and chemotherapy kept | the source's use case and features | prognosis given treatment, not a guide to choosing it |
     | B | At diagnosis | treatment columns dropped | a prediction before any treatment | not the source's use case; weaker |

   * **Recommendation:** A. **Decision:** A or B?

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: the prediction point is after first-course treatment; surgery, radiation and chemotherapy stay.

   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then. A value that did not exist at that point is a leak.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.
