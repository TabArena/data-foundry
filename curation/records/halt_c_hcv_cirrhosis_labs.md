---
unique_name: halt_c_hcv_cirrhosis_labs
name: HALT-C trial (Hepatitis C Antiviral Long-term Treatment against Cirrhosis), NIDDK Central Repository; the cirrhosis-from-standard-labs analysis of ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1002/hep.20772
- https://repository.niddk.nih.gov/studies/halt-c/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a published cirrhosis-from-routine-labs model (Lok et al. 2005) on 1,141 biopsy-staged hepatitis C patients of the NIH HALT-C trial; the data is on request from the NIDDK Central Repository, and every patient had advanced fibrosis.
- Source: the HALT-C trial (Hepatitis C Antiviral Long-term Treatment against Cirrhosis), NIDDK; enrollment and data collection June 2000 to October 2009 at 12 sites, 1,382 participants; the NIDDK Central Repository holds 174 datasets (screening baseline, lead-in and randomized phase, biopsy, analysis datasets) with a codebook, protocol and manual of operations (repository.niddk.nih.gov/studies/halt-c). The analysis that defines this task: Lok, Ghany, Goodman et al., "Predicting cirrhosis in patients with hepatitis C based on standard laboratory tests: results of the HALT-C cohort", Hepatology 42(2):282-292 (2005), doi 10.1002/hep.20772. There: 1,141 patients with a stageable baseline biopsy (4 of 1,145 excluded), 429 (38%) with cirrhosis (Ishak 5-6) against bridging fibrosis (Ishak 3-4, plus 97 Ishak-2 patients whose earlier biopsy showed bridging); training 783, validation 358; candidates BMI, spleen size on ultrasound, lifetime alcohol and most routine labs; the final logistic model uses platelets, AST/ALT ratio and INR. Tables to join by patient: baseline labs, demographics, the biopsy reading.
- Use case: a hepatologist decides from routine blood tests whether a chronic hepatitis C patient has cirrhosis (and so needs HCC and varices surveillance) without a liver biopsy; the paper's cutoffs (below 0.2 to exclude, above 0.5 to confirm) are that decision. Fit approximate: entry required bridging fibrosis or cirrhosis and failure of earlier interferon, so the stage range is narrower than in the clinics where such a model is used (`Selection Bias`). Regime IID, one baseline biopsy per patient (the 12 sites allow a grouped check).
- Siblings and duplicates: `hepatitis_c_egypt` (`No`, AHDS and Data Quality Issue: the UCI file behaves like generated data), `hepatitis_c_prediction` (`Yes`, Selection Bias: another source and population), `nhanes_liver_elastography_fibrosis` (a candidate of this run: fibrosis by FibroScan in a national sample, another source, PROV-7); no other HALT-C record (`grep -il halt-c` over `curation/records/`). External collections: none found.
- Better data: found as better data for `hepatitis_c_egypt`; no further search this round.
- Papers and pages: Lok et al. 2005 (full text on Deep Blue, deepblue.lib.umich.edu/bitstream/2027.42/48683/1/20772_ftp.pdf; summary on natap.org); the Lok index is in clinical calculators (MSD Manuals, "Cirrhosis Probability in Hepatitis C").
- Metric: the AUROC of the final model, 0.78 in training and 0.81 in validation (Lok et al. 2005, Results), the paper's one discrimination measure, with two cutoffs reported next to it; so `roc_auc` (MET-5; the binary fallback agrees). The cutoffs are a two-sided rule, not one fixed threshold (MET-6). Inputs none.
- Risks for /add-dataset: access is a data request to NIDDK-CR under a use agreement and a Certificate of Confidentiality (no criterion, EV-4; the add stage waits for it, and the repository page says it is "under review for potential modification"); joins across the repository's datasets by patient, with the baseline visit fixed so no lab of the randomized phase enters (LEAK); the target: cirrhosis yes or no on the central pathologists' Ishak stage, or the stage itself (the curator's call); the trial predates direct-acting antivirals (`Outdated` to weigh).
- Priority: gap 0 (medical and binary not thin), use case + (the paper names the decision and its cutoffs), source + (NIH repository with codebook, a peer-reviewed analysis), shape + (1,141 patients, labs plus demographics and clinical items), risk - (joins across repository datasets, a request-only release).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `hepatitis_c_egypt`.
- as published: 1,382 participants in the repository (174 datasets: screening baseline, lead-in, randomized phase, biopsy, analysis datasets); Lok et al. used 1,141 patients with a baseline biopsy, 429 with ...; target: cirrhosis on the baseline liver biopsy (consensus fibrosis stage read by a blinded pathologist panel), or the fibrosis stage itself; access: request.
- Why: the task the Egyptian file claims (fibrosis stage of hepatitis C patients from non-invasive tests) on real, biopsy-staged patients; features of the same kind (platelets, AST, ALT, INR, albumin, age, sex), all measured before the biopsy result is known; the published model reached AUROC 0.78-0.81 with platelets, ...
- Adds: real and traceable patient records where the UCI file behaves like generated data; a biopsy-staged label read centrally; about the same size (1,141 vs 1,385). Caveats: all patients had advanced fibrosis (bridging fibrosis or cirrhosis) and had failed interferon, so the stage range is narrower than F1-F4; access on ...
