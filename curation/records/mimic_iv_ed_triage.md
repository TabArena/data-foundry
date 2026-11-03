---
unique_name: mimic_iv_ed_triage
name: MIMIC-IV-ED benchmark (ED triage prediction)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1038/s41597-022-01782-9
- https://doi.org/10.13026/1cjn-2370
- https://github.com/nliulab/mimic4ed-benchmark
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a published ED benchmark (Xie et al. 2022) that defines triage outcomes with a fixed prediction point on 441,437 adult visits of MIMIC-IV-ED, built by an open script from two credentialed PhysioNet databases; its master table also holds ED-stay columns that a triage task must drop.
- Source: MIMIC-IV-ED, Johnson, Bulgarelli, Pollard, Celi, Mark & Horng, PhysioNet (v1.0 of 2021-06-03; v2.2 of 2023-01-05, https://doi.org/10.13026/5ntk-km72; the record's DOI 10.13026/1cjn-2370 resolves to the latest version): "about 425,000" ED stays at Beth Israel Deaconess, 2011-2019, six tables (edstays, diagnosis, medrecon, pyxis, triage, vitalsign), credentialed access under the PhysioNet DUA. The task: Xie et al., "Benchmarking emergency department prediction models with machine learning and public electronic health records", Sci Data 2022 (https://doi.org/10.1038/s41597-022-01782-9, PMC9610299), with its script at github.com/nliulab/mimic4ed-benchmark (GPL-3.0; written for MIMIC-IV v1.0 and MIMIC-IV-ED v1.0). As published: a master table of 448,972 ED visits of 216,877 patients with 81 columns (README), filtered to 441,437 adult visits with a triage class; outcomes hospitalisation (208,976 visits, 47%), critical outcome, i.e. inpatient death or ICU transfer within 12 h (26,174, 5.9%), and 72-hour ED reattendance (15,299, 3.5%) (Results, Table 2).
- Use case: the paper's: "Predicting the critical outcome at ED triage may enable physicians to allocate ED resources efficiently and intervene on high-risk patients promptly", and hospitalisation "may facilitate resource allocation efforts" (Methods, "Benchmark tasks"); actor the triage nurse or ED physician, moment triage, decision acuity and an early bed request; fit direct for hospitalisation and critical outcome at triage (the reattendance task predicts at ED disposition, another prediction point). Regime grouped by patient: 216,877 patients make 448,972 visits and prior-visit counts are features; the paper's split ("randomly split into 80% (353,150) training data and 20% (88,287) test data", Results) is by visit, a claim (SPLIT-5); a temporal split works only through `anchor_year_group`, since MIMIC shifts each patient's dates.
- Siblings and duplicates: `mimic_iv` (`TBD -> 2nd Tier`, priority 2, the database without a task) shares the source; this record is one defined task of its ED module, a distinct task and no duplicate (PROV-7); the curator may let this record carry MIMIC-IV's ED tasks. The same task family from other sources, no copies (PROV-4): `nhamcs_ed_hospitalization` (NHAMCS survey), `curial_covid_ed_triage`, `ed_uti_urine_culture_prediction`. External collections: none among the records; the web was not searched (search budget used up).
- Better data: found as better data for `mimic_iv`, and in the curator's Zotero collection (item 80, "PhysioNet"); no further search this run.
- Papers and pages: the PhysioNet page of MIMIC-IV-ED; Xie et al. 2022 (full text read on Europe PMC); the benchmark repository's README.
- Metric: Xie et al. report AUROC and AUPRC "as an overall measurement of predictive performance", plus sensitivity and specificity "under the optimal cutoffs, defined as the points nearest to the upper-left corner of the ROC curves" (Methods, "Experiments, settings, and evaluation"): several metrics side by side and a cutoff chosen on the data, not by the decision, so the fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none.
- Risks for /add-dataset: the master table holds "variables collected at triage and during ED stay, and primary ED-relevant outcomes" (Methods, "Master data generation"): ED length of stay, ED vitals, medications and the disposition go for a triage task (USE-3); the chief complaint is free text in `triage` (the benchmark makes flags of it); the script targets v1.0 of both databases (v2.2 changes the counts); one target per dataset (hospitalisation and critical outcome are distinct tasks, PROV-7); start from the master table before the benchmark's imputation; credentialed access and a DUA that bars redistribution (EV-4, noted only).
- Priority: gap 0 (medical & healthcare, binary, grouped not thin), use case + (the paper names the triage decision), source + (a PhysioNet release and a Scientific Data paper with code), shape + (441,437 visits; vitals, acuity, complaints, history counts), risk - (post-triage columns in the master table; two credentialed databases joined by script): 3.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mimic_iv`; the curator's Zotero collection, item 80: "PhysioNet".
- as published: about 425,000 ED stays at Beth Israel Deaconess, 2011-2019 (MIMIC-IV-ED); the benchmark script builds one table of triage vitals, chief complaint, demographics and prior-visit counts; target: hospitalisation at triage; critical outcome (ICU or death within 12 h); ED revisit within 72 h; access: registration.
- Why: Published benchmark tasks with a fixed prediction point on a large real ED cohort.
- Adds: Emergency triage at scale; gives the mimic_iv record a defined task. Caveats: credentialed, built by script from MIMIC-IV-ED + MIMIC-IV.
