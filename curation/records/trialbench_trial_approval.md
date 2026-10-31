---
unique_name: trialbench_trial_approval
name: 'TrialBench: Benchmarking Multi-Modal Artificial-Intelligence-Ready Clinical Trial Prediction'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2024'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zenodo.org/records/14975339
- https://arxiv.org/abs/2407.00631
- https://huyjj.github.io/Trialbench/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: TrialBench's trial-approval table (43,202 ClinicalTrials.gov trials registered before 2024-02-16, labels from the HINT benchmark's TrialTrove subset and from registry termination reasons), the outcome task `clinical_trials` lacks; free-text and SMILES columns and a random published split to rework.
- Source: Chen, Hu, ..., Zitnik and Fu, "TrialBench: Multi-Modal AI-Ready Clinical Trial Datasets", arXiv 2407.00631 (v1 2024-06-30, v3 2025-06-15, "accepted by Nature Scientific Data"); data on Zenodo 14975339 (2025-03-05, CC BY 4.0; trial-approval-forecasting.zip, 43.5 MB) and huyjj.github.io/Trialbench. As published: 23 datasets for 8 tasks, cut by phase; trial approval forecasting is binary, 43,202 trials, "all 5 modalities" (categorical and numerical fields, free text such as eligibility criteria, MeSH terms, ICD-10 codes, drug SMILES from DrugBank). The paper: "we ensured that trial result information was not included if the AI task is to be performed before trial completion"; the labels: "First, the HINT paper ... builds a benchmark dataset for trial approval prediction, with approval labels sourced from TrialTrove. Additionally, ClinicalTrials.gov provides termination reasons".
- Use case: a sponsor or investor decides at registration whether to run or fund a trial, from its design (the paper's definition: "Whether a drug can pass a certain phase of the clinical trial"); fit approximate, since the label pools TrialTrove outcomes and registry termination reasons. Regime temporal by start or registration date: the paper's "random splitting ... 8:2" is a claim (SPLIT-5), and recent trials have unmatured outcomes (SPLIT-9).
- Siblings and duplicates: `clinical_trials` (`TBD -> 2nd Tier`, `No Good Target (yet)`; a 13K-trial Kaggle extract of ClinicalTrials.gov without a target) is the record it was found for; `covid_trials` (`No`, `No Good Target / Scientific Discovery`). The HINT TOP benchmark (Fu et al., Patterns 3:100445, 2022; github.com/futianfan/clinical-trial-outcome-prediction) first published the approval labels TrialBench reuses and has no record. The other TrialBench tasks (duration, dropout, adverse events, mortality, failure reason) are distinct targets on the same registry (PROV-7). External collections: TrialBench; PyTrial and PyTDC carry TOP.
- Better data: found as better data for `clinical_trials`.
- Papers and pages: the TrialBench paper (read: Data Acquisition, Data Partitioning, Evaluation Metrics, Table 6); HINT (Fu et al. 2022).
- Metric: the paper reports accuracy, PR-AUC, F1 and ROC-AUC side by side for every classification task (Evaluation Metrics, Table 6) and names no criterion, so the fallback `roc_auc` (MET-5); inputs none.
- Risks for /add-dataset: two labelling processes (TrialTrove outcomes and registry termination reasons) may differ in which trials and fields they cover (USE-5; check for class-dependent recording, LEAK-13); free-text eligibility criteria and summaries (SEL-12: keep the structured fields, drop or encode the text) and SMILES (descriptors); the phase cut (one dataset with phase as a feature, or one phase); registry fields updated after registration (actual against anticipated enrollment, status) to check at the prediction point (LEAK-10); TOP as the first publication of the labels (PROV-8).
- Priority: gap 0 (medical, binary and temporal are well covered), use case 0 (the paper names the task, not who acts), source + (a paper with a documented build and a Zenodo release), shape + (43,202 trials, mixed fields, dates), risk - (label provenance, text columns, published random split).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `clinical_trials`.
- as published: ClinicalTrials.gov trials registered before 2024-02-16, one table per task: trial approval about 43.2K trials, failure reason about 41.4K, patient dropout about 62.1K, duration about 141.9K, serious ...; target: trial approval or success (binary), with failure reason, dropout and adverse-event targets in the other tables; access: open.
- Why: The record is a 13K-trial ClinicalTrials.gov extract with no target, and it notes that a termination or outcome task would need its own build from the registry. TrialBench is that build: trials taken from the same registry, with outcome labels and with features known at registration
- Adds: A defined target and a published benchmark; 3x the trials for the approval task. Risks: some columns are free text and SMILES (SEL-12), and the approval labels come from a TrialTrove subset whose terms are non-commercial. Without the text columns it is a structured table
