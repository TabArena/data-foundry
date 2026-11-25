---
unique_name: pheochromocytoma_paraganglioma_metastasis
name: Metastatic pheochromocytoma and paraganglioma (Pamporaki et al. 2023, Zenodo 7749613)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
original_source: Other
year: '2023'
collection_period: Unknown
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.7749613
- https://www.nature.com/articles/s41467-024-45879-8
- https://doi.org/10.1186/s12911-026-03654-3
- https://doi.org/10.1016/S2589-7500(23)00094-8
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: real, documented cohorts of pheochromocytoma and paraganglioma patients (Pamporaki et al. 2023, Lancet Digit Health; Zenodo, CC BY 4.0), 788 patients, nine preoperative clinical and biochemical features plus SDHB status, target metastatic disease; a small but clean clinical task with a stated preoperative use case and two cohorts.
- Source: Pamporaki, Berends, Filippatos, Prodanov, Meuter, Prejbisz et al., "Prediction of metastatic pheochromocytoma and paraganglioma: a machine learning modelling study using data from a cross-sectional cohort", Lancet Digit Health 5:e551-e559 (2023), doi 10.1016/S2589-7500(23)00094-8 (read from PMC10565306); data: Zenodo 10.5281/zenodo.7749613, `DataZonodo.xlsx`, published 2023-03-19, CC BY 4.0 ("The data generated in this study are available in the online platform (zenodo...)", Data availability). As published (previewed): one sheet, 788 patients x 40 columns: `Patient ID`, `Internal Testing (IT)/External Validatio (EV)` (493 IT, 295 EV), sex, age at diagnosis of first tumour, `Predictions for metastatic disease` (EV only: the prospective methoxytyramine call, values NO / YES-possible / YES-moderate / YES-strong / "false negative"), plasma normetanephrine, metanephrine and methoxytyramine, previous history of PPGL, adrenal or extra-adrenal location, `Presence of SDHB` (NO 596, YES 112, "not tested" 80), tumour category (single, bilateral, multifocal), spherical tumour volume, target `Metastatic YES/NO` (IT 166 of 493, EV 57 of 295), then 24 columns of the 12 specialists' risk calls without and with SDHB. Contrary to the data scout's note, the external validation cohort (295 PMT patients) is in the file: "The best candidate ML models were then externally validated using the dataset of 295 patients with PPGL who were enrolled in the PMT-trial ... These included the 267 patients with positive test results and another 28 with negative test results" (Methods).
- Use case: "these models allow for predictions at first diagnosis of PPGL by utilizing clinical features routinely and preoperatively available"; "identifying patients with low probabilities of metastases, who may then be excluded from intensive, long-term and costly follow-up programs, our ML models provide justification for preoperative functional imaging and extensive follow-up in patients with high probability of metastases" (Discussion). Actor: an endocrinologist at first diagnosis, deciding functional imaging and follow-up intensity; fit direct. Collection: patients enrolled over years in the NIH protocol 00-CH-0093, the PRESCRIPT trial and the prospective PMT trial (Germany, Poland, the Netherlands), no date per row (`Samples: Over Time`, `Time: Lost`); metastases are "the presence of metastases in tissues distant from the primary tumor" found at diagnosis or during follow-up of varying length (`Target: Varying Delay`; "The shorter duration of follow-up among patients without compared to those with metastases in the prospective PMT cohort"); type Clinical Study.
- Split: leaf [L-PLACE.random] (Random · `ForcedIIDFromGrouped`, the transfer untested) because [CLI.meets] the source's use is at other centres (it trains on NIH and PRESCRIPT patients and validates on the PMT cohort), [PLACE.several] the release holds two cohorts (the IT/EV column), short of the enough-groups check, with no centre or country column, [PLACE.units] one row per patient. Open: whether to ship the source's IT-to-EV split as a recorded departure (Arasteh kept it; Shaktah drew a random split); prevalence differs by cohort (34% against 19%).
- Siblings and duplicates: none among `curation/records/` (grep pheochromocytoma, paraganglioma, Pamporaki, methoxytyramine). Arasteh et al. 2024 used the same file with "the same (training and test) dataset distribution as the original study" (Results, "Metastatic disease"), 493 and 295 patients; Shaktah et al. 2026 read a CSV of the sheet, dropped only `Predictions for metastatic disease`, the target text and the ID, and split at random (`TabPFN_MetDis_CPU.py`, `KeepSplit = False`), and its script drops neither the IT/EV flag nor the 24 specialist-prediction columns (whether a shared helper does was not checked). Both are copies (PROV-4, PROV-8): /add-dataset starts from the Zenodo file. External collections: Arasteh et al. 2024; Shaktah et al. 2026.
- Better data: none found (data scout, 2026-11-25: Zenodo, figshare, the TU Dresden research portal, the web). Later work is imaging-based (CT radiomics, Insights Imaging 2025) or molecular (figshare 25792479, 79 SDHB patients, multi-omic), not the same task.
- Papers and pages: Pamporaki et al. 2023 (ensemble tree classifier AUC 0.942 on the external cohort against 0.815 for the best specialist); Arasteh et al. 2024 (GBM 0.949, re-implemented AdaBoost 0.951); Shaktah et al. 2026 (CatBoost 0.934, LR 0.928, TabPFN 0.918).
- Metric: the paper reports AUC, MCC and balanced accuracy ("The best performing ENS model, which had an AUC of 0.942 ..., an MCC of 0.851 and a balanced accuracy of 88%", Results) and chose the final model on "the best MCC and balanced accuracy metrics" (Discussion), threshold metrics at no threshold fixed by a decision: several reported, so the fallback `roc_auc` (MET-5, MET-6); inputs none.
- Risks for /add-dataset: drop `Predictions for metastatic disease` (EV only; its "false negative" value is written with hindsight) and the 24 specialist columns (LEAK-10; they are the paper's comparators); `Presence of SDHB` is "often not available at initial diagnosis" (Discussion) and "not tested" for 80 patients: keep as the paper's ten-feature variant or drop for the nine-feature one, a USE-3 call; `Previous history of PPGLs` marks recurrent patients, more common in the training cohort; outcome ascertainment shorter in the prospective cohort (label noise towards "no"); size 788 (TP-5 is fine at 223 positives).
- Priority: gap 0 (medical, binary), use case + (named actor and decision, direct), source + (Lancet Digit Health, CC BY deposit), shape 0 (788 patients, 10 features), no risk point (the leaky columns are named and droppable).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.

## Review

**Outcome:** not added; screened `TBD -> Yes`, priority 3. Pamporaki et al. 2023 (Zenodo, CC BY 4.0): 788 patients, nine preoperative features plus SDHB status, metastatic disease in two cohorts; the 24 specialist calls and the external cohort's prediction column go.

**Main points:** Keep SDHB status as a feature (issue 1); random split or the source's internal-to-external split (issue 2).

**Issues for Andrej:**

1. **Keep SDHB status as a feature?**

   * **Problem:**
     - The paper's best model uses ten features with SDHB, but the Discussion calls SDHB "often not available at initial diagnosis", the prediction point of the use case[^use3].
     - 80 of 788 patients are "not tested"; the paper also reports a nine-feature model without it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep SDHB, with "not tested" as its own value (implemented) | the paper's ten-feature model | the source's main task; "not tested" is what the endocrinologist knows | SDHB known for most patients here, more than at a first visit |
     | B | Drop SDHB | the paper's nine-feature model | holds only what every first visit has | weaker than the source's main model |

   * **Recommendation:** A: the test is ordered at diagnosis in the source's centres, and "not tested" keeps the missing case honest. **Decision:** A or B?

   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then. A value that did not exist at that point is a leak.

2. **Random split, or the source's internal-to-external split?**

   * **Problem:**
     - The release holds two cohorts (493 internal, 295 external, metastatic 34% and 19%) and no centre column, so the split tree reaches a forced random leaf[^split36].
     - Arasteh's 2024 benchmark kept the source's split, and Shaktah's drew a random one.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Repeated 3-fold cross-validation on all 788 (implemented) | the forced random leaf; the cohort flag is no feature | varied training sides; uses every patient | transfer to a new centre untested |
     | B | The source's split as a recorded departure | train on 493, test on 295 | the source's validation; tests transfer to the prospective cohort | one training side only; 57 test positives |

   * **Recommendation:** A: a single fixed split gives one training side, and two cohorts are too few groups to test transfer. **Decision:** A or B?

   [^split36]: **SPLIT-36** (Should): a definition's split is decided by walking the split decision tree; a forced leaf is for the curator to look at.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.
