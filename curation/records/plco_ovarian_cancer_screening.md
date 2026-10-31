---
unique_name: plco_ovarian_cancer_screening
name: PLCO Cancer Screening Trial, Ovarian dataset (NCI CDAS)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://cdas.cancer.gov/plco/
- https://cdas.cancer.gov/datasets/plco/23/
- https://doi.org/10.1001/jama.2011.766
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 78,216 women of the PLCO trial (1993-2001) with annual CA-125 and transvaginal ultrasound results in the screened arm and confirmed ovarian cancer over up to 13 years; a real screening cohort with few positives (388 cancers). The record also held the PLCO Prostate dataset, a separate task, now named apart.
- Record: the merge of the scouts' hits put two PLCO datasets into this record (the title said "Prostate dataset", the unique name says ovarian). This block screens the PLCO Ovarian dataset and the title now says so. The Prostate links moved here from `source_links`, for a record of their own (`plco_prostate_cancer_screening`, the merge's alias; a distinct task, PROV-7), found as better data for `prostate_cancer_detection`: https://cdas.cancer.gov/datasets/plco/20/ (PLCO Prostate: one row per man, about 77,000; Prostate Screening about 177,000 rows with the annual PSA and DRE) and Andriole et al., "Mortality Results from a Randomized Prostate-Cancer Screening Trial", NEJM 2009 (https://doi.org/10.1056/NEJMoa0810696).
- Source: the PLCO Cancer Screening Trial of the National Cancer Institute, through the Cancer Data Access System (cdas.cancer.gov/plco/); the ovarian results in Buys et al., "Effect of Screening on Ovarian Cancer Mortality", JAMA 2011 (doi 10.1001/jama.2011.766; abstract read). As published (cdas.cancer.gov/datasets/plco/23/): Ovarian (one row per woman, about 78,000), Ovarian Screening (about 151,000, one per screening year, "additional information from the Transvaginal Ultrasound (TVU) and CA-125 screens"), Screening Abnormalities (20,000), Diagnostic Procedures (19,000), Medical Complications (700), Treatments (1,900); dictionaries tagged 2024-10-11. Buys et al.: 78,216 women aged 55-74 at 10 centres, 39,105 offered "annual screening with CA-125 for 6 years and transvaginal ultrasound for 4 years"; ovarian cancer in 212 women of the screened arm and 176 of usual care; 3,285 women with false-positive results, 1,080 of them with surgical follow-up.
- Use case: after a screening round, the woman's practitioner decides whether an abnormal CA-125 or ultrasound result goes to surgical work-up ("Participants and their health care practitioners received the screening test results and managed evaluation of abnormal results", Buys et al.); fit direct; regime grouped by woman for a task per screen (up to six screens each), or IID for a task per woman from the baseline questionnaire (to decide).
- Siblings and duplicates: `ovarian_cancer_prediction` (`No`, `Trivial`: 253 SELDI serum spectra), `plco_lung_cancer_incidence` (the same trial, another file and cancer: PROV-7); no duplicate. External collections: none found.
- Better data: found as better data for `ovarian_cancer_prediction` (and, before the split above, for `prostate_cancer_detection`) in the data-scouting run of 2026-10-30/31; no further search this round.
- Papers and pages: Buys et al. 2011; the CDAS pages. Not opened: the ovarian dictionaries and the later PLCO papers on CA-125 risk algorithms.
- Metric: none found for a prediction (Buys et al. report mortality and incidence rate ratios and the harms of work-up), so the fallback `roc_auc` (MET-8); inputs none (a woman id ships for grouping).
- Risks for /add-dataset: few positives (388 cancers in 13 years, fewer within a year of a screen): count them per test fold first (TP-5); build the label (cancer within a set time after a screen, or within a horizon from baseline) from the diagnosis days; drop the work-up, staging and treatment fields (LEAK-10); the trial's positive-screen rule is a threshold on CA-125 or an abnormal ultrasound (35 U/mL from memory, check the dictionary), so the task has to beat that rule (TP-4); join the person and screening files; access through a CDAS project proposal, terms not read (a practical point, EV-4).
- Priority: gap 0 (medical and binary are not thin), use case + (the work-up decision named by the trial), source + (NCI, the JAMA trial report), shape + (78,216 women, about 151,000 screens), risk - (a rare outcome, and a label and screen rows to build).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ovarian_cancer_prediction`, `prostate_cancer_detection`.
- as published: Prostate file one row per man (~77,000, CDAS page), Prostate Screening one row per screening year (~177,000: annual PSA for 6 years, DRE for 4 years in the screening arm), diagnostic procedures ...; target: Prostate cancer diagnosed after a screening round (e.g. within one year of the screen); access: request (CDAS project proposal, then a Data Transfer and Use Agreement).
- Why: The same target (prostate cancer vs none in screened men) from a blood test known at the screening visit; the features are PSA and DRE results instead of a SELDI spectrum, the same kind (serum measurement at the visit) measured with a standard assay. | The same target (ovarian cancer vs none) from a serum test known ...
- Adds: About 240 times more men, a real screening population instead of case groups from different sites, and none of the processing artefacts that retired prostate_cancer_detection (classes processed separately, Baggerly et al. 2004). | About 300 times more women than the 253 serum spectra, a prospective screening cohort ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the run merged the PLCO Prostate data into this record; its links moved to the comments, and it needs its own record (`plco_prostate_cancer_screening`).
