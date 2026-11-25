---
unique_name: seer_osteosarcoma_survival
name: 'SEER osteosarcoma (C40-C41): 5-year survival'
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
- https://doi.org/10.1097/MD.0000000000039582
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: five-year overall survival of primary bone tumours in the NCI SEER registries; real and documented, but a small cohort when restricted to osteosarcoma (1,243 patients of 2000-2018 in the paper it reproduces), Shaktah's extract takes every tumour of Primary Site C40-C41 and keeps patients alive under five years out only when they lived, and it is the second SEER five-year survival task after `seer_breast_cancer_5y_survival`.
- Source: National Cancer Institute, SEER Program, "Incidence - SEER Research Data, 17 Registries, Nov 2024 Sub (2000-2022)" (Shaktah et al. 2026, Methods, "Datasets": "OST survival; ... Primary Site C40.0-C41.9"; no histology filter is named, and the code applies none). SEER Research Data is per person through SEER*Stat after acknowledging the SEER Research Data Use Agreement ("Each person who will access the data must submit a separate request", seer.cancer.gov/data/access.html). The agreement (November 2025 submission) says in clause 10 "Authorized User will not release, nor permit others to release, the Data to any other person", and its clause 19 ("Permitted Use of AI/ML Tools") allows approved users to "develop or validate analytical and generative AI models using the Data" within an approved request, but "may not share the model, including model parameters, except with collaborators who are also Approved Users" and may not use the data with any tool "that transmits data to an external provider": a release-checklist item, no criterion (EV-4), but no row of it can ship and every user must extract it themselves. As published: case listings, one row per tumour (fields as for the other SEER records: year of diagnosis, age, sex, race, site, histology, grade, tumour size, stage, mets at DX (2010+), first-course surgery, radiation, chemotherapy, survival months, vital status, cause of death). The target in Shaktah's code (`SEER_OST/TabPFN_SEER-OST_CPU.py`): `np.where(df2["Survival months"] >= 60, 1, np.where(df2["Vital status recode (study cutoff used)"].astype(str).isin(["Dead"]), 0, np.nan))`: alive under 60 months is missing, so a recent diagnosis enters only if the patient died; "Year of diagnosis" is not dropped (Supplemental List 1 drops only cause of death, survival months and flag, vital status).
- Use case: the paper it reproduces, Cao, Dun, Xiang, Wang, Cheng, Yan et al., "Machine learning-based individualized survival prediction model for prognosis in osteosarcoma: Data from the SEER database", Medicine 103:e39582 (2024), doi 10.1097/MD.0000000000039582, read from Europe PMC full text: "From 2000 to 2018, 1243 patients with osteosarcoma were collected" (Abstract); "Training data was used to train the ML algorithms that consider time to event with the overall survival (OS) as the outcome" (Methods); "we use models to make treatment recommendations of systematic therapy (chemotherapy) options for osteosarcoma patients" (Methods, "Treatment recommendation"). Actor: an orthopaedic oncologist after diagnosis weighing prognosis and systemic therapy; fit approximate (the treatment is a feature, so the model informs prognosis given the treatment, not the choice). Collection: samples over time dated by year of diagnosis; target after a fixed 60-month window; a patient can hold several tumours; cases resubmitted with recodes; type Dated Event Log (SPLIT-34 rule 3).
- Split: leaf [L-ORDER.windows] (Temporal · windows on the time key) because [LOG.meets] later patients, [ORDER.order] year of diagnosis, [ORDER.windows] about 20 diagnosis years; gap five years by the gap rules (an outcome window still open: train only on diagnoses whose 60 months have closed before the window's scoring date). Open: [ORDER.windows] whether yearly windows of osteosarcoma alone (about 60-100 cases a year) reach the scored units of SPLIT-33, else wider windows or [ORDER.exception], a person's call; the window length (SPLIT-12).
- Siblings and duplicates: `seer_breast_cancer_5y_survival` (`TBD -> Yes`, 3: the same registry, five-year breast-cancer-specific death), `seer_breast_cancer_survival` (`TBD -> 2nd Tier`, 2: a 4,024-row DataPort cut of it, a PROV-6 version of the former), `seer_primary_site_from_metastases` (`TBD -> Yes`, 3: another task on the same registry, PROV-7), `fosp_cancer_registry_survival` (`TBD -> Yes`, 2: São Paulo registry, survival by site, which left "one dataset per cancer site or all sites with the topography as a feature" open). The siblings' precedent is one record per task on SEER (PROV-7: distinct cohorts and targets), not one SEER record. Same task type as `seer_breast_cancer_5y_survival` and `seer_renal_cell_carcinoma_5y_survival` on disjoint patients (other organ, other features: bone site, Enneking-relevant extent), so not a duplicate (PROV-7); whether the benchmark takes more than one or two SEER five-year survival tasks is the curator's call. External collections: Shaktah et al. 2026 benchmark (not in our vocabulary).
- Better data: none from another source (data scout, 2026-11-25: no public row-level registry beyond SEER; NCDB and the English, Taiwanese and NPCR survival files are restricted). Newer versions of this source (PROV-6): SEER Research Data, 17 Registries, Nov 2025 submission (diagnoses 2000-2023, released April 2026); the 21-registry Limited-Field file is wider (about 1.7x the tumours) but drops AJCC TNM, the radiation recode and marital status, and has survival fields only in its SEER 21 (excl. IL) variant.
- Papers and pages: Shaktah et al. 2026 (AUROC GradientBoosting 0.809, LR 0.748, TabPFN 0.802; 70/30 random split); Cao et al. 2024 (DeepSurv C-index 0.74, 5-year AUC 0.78, 7:3 random split: "In a 7:3 random split, the dataset was used for training and for validating models"); an earlier 5-year osteosarcoma model on SEER with XGBoost (Sci Rep 2021, PMC7970935, not read).
- Metric: Cao et al. assess "the concordance index (C-index), the Integrated Brier Score (IBS), receiver operating characteristic curves (ROC), area under the ROC curves (AUC), calibration curves, and decision curve analysis" (Abstract): several reported, the C-index for the time-to-event model, the 5-year AUC for this horizon; Shaktah AUROC. The fallback `roc_auc` on the binary 5-year label (MET-1, MET-5, MET-8); inputs none.
- Risks for /add-dataset: restrict to diagnoses with five years of potential follow-up (the Nov 2024 submission follows to the end of 2022, so diagnoses to 2017; Nov 2025 to 2018) or the recent years hold only deaths and the year of diagnosis becomes a shortcut (SPLIT-9, LEAK, `Class-dependent Recording`); alive under 60 months in old years is loss to follow-up (count it); cohort: osteosarcoma histology (ICD-O-3 9180-9187, 9192-9195) as in Cao et al., or all primary bone tumours as Shaktah's C40-C41 extract (chondrosarcoma, Ewing sarcoma, chordoma, myeloma of bone?), to decide (USE-5); survival months, vital status and cause-of-death columns go (LEAK); first-course surgery, radiation and chemotherapy set the prediction point after treatment planning (USE-3); the SEER radiation and chemotherapy fields are "yes" against "no/unknown" (Treatment Data Limitations); size (TP-8). Release: the Research 17-registry Nov 2025 submission (2000-2023) is the newest; in the 21-registry Limited-Field database survival months, vital status and cause of death are "No*" ("available in the SEER 21 (excl IL) Limited-field database") and AJCC TNM, radiation and marital status absent (variable dictionary, Nov 2025). The agreement bars shipping rows (above).
- Priority: gap 0 (medical, binary, temporal not thin), use case 0 (approximate; treatment as an input), source + (NCI SEER, two papers), shape + (about 1,000-2,500 osteosarcoma cases with follow-up, more for all bone tumours; mixed types), risk - (cohort to define; censoring shortcut through the year).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.

CC (2026-11-25, Andrej): accepted for adding in the screening review (issue 2 A (one-year windows); issue 1 (cohort) open until the use case is written at /add-dataset).

## Review

**Outcome:** not added; screened `TBD -> 2nd Tier`, priority 2. Five-year overall survival of bone tumours in SEER; small when restricted to osteosarcoma (1,243 patients of 2000-2018 in Cao et al. 2024), and Shaktah's label keeps a recent patient only when they died (the cohort is cut where five years of follow-up are complete).

**Main points:** Osteosarcoma only or all bone tumours (issue 1); window length (issue 2).

**Issues for Andrej:**

1. **Osteosarcoma only, or every primary bone tumour?**

   * **Problem:**
     - Cao et al., the paper Shaktah reproduces, take osteosarcoma (1,243 patients); Shaktah's extract takes all of Primary Site C40-C41 (chondrosarcoma, Ewing sarcoma, chordoma and others) with no histology filter[^use5].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Osteosarcoma histology (implemented) | ICD-O-3 9180-9187, 9192-9195, as Cao et al. | the source task; one disease and its oncologist | about 60-100 cases a year |
     | B | All primary bone tumours | histology as a feature | several times the rows | several diseases with different treatments in one label |

   * **Recommendation:** A. **Decision:** A or B?

   **Andrej (2026-11-25, discuss):** Decide depending on the use case that is created and once the task is built raise this in the dataset's review.

   **Answer (AI, 2026-11-25):** agreed; the issue stays open until the task is built.

   * /add-dataset writes the use case first, builds osteosarcoma only and all bone tumours side by side, and brings the case and death counts per window and the two scores back to this issue in the added dataset's review.
   * Your answer to the consistency check on kidney cancer issue 1 (one cancer or the whole site) applies here too.

   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it. Check how the source built its label before accepting it.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.

2. **Window length for the temporal split?**

   * **Problem:**
     - Labels mature five years after diagnosis, so train only on diagnoses whose five years closed before the test window[^leak24].
     - Yearly windows of osteosarcoma hold about 60-100 cases each, perhaps too few deaths per window[^split12].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One diagnosis year (implemented) | yearly windows, five-year gap | follows a yearly refit | small test windows |
     | B | Two or three diagnosis years | wider windows, five-year gap | steadier scores | fewer windows |

   * **Recommendation:** A, unless the case counts per year at /add-dataset fall too low; then B. **Decision:** A or B?

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: one-year test windows by diagnosis year, five-year gap; /add-dataset reports the cases and deaths per window.

   [^leak24]: **LEAK-24** (Must): a target right-censored in the newest periods (a duration or a final status cut by the download date) is cut where follow-up is complete, or re-sourced from an archive with settled labels.
   [^split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source: how far ahead the actor predicts, the competition's own test window, the refit cadence. Choose the test windows to match it.
