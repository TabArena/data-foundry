---
unique_name: gut_cirrhosis_metaml
name: gut-cirrhosis (Gut microbiome markers, healthy vs cirrhosis)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Many features
- Tiny Data
collections:
- TabBench-Bio
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.1038/nature13568
- https://github.com/segatalab/metaml
- https://arxiv.org/abs/2609.07441
- https://doi.org/10.1371/journal.pcbi.1004977
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: liver cirrhosis against healthy controls from stool strain-marker presence (the Qin et al. 2014 cohort as packaged by MetAML); a real diagnostic aim, but the same 232 samples and target as `gut_microbiome_liver_cirrhosis`, which uses the species abundances (PROV-6).
- Source: Qin, Yang, Li et al., "Alterations of the human gut microbiome in liver cirrhosis", Nature 513:59-64, online 2014-07-23 (https://doi.org/10.1038/nature13568; abstract read on PubMed 25079328, full text paywalled); packaged by MetAML: Pasolli, Truong, Malik, Waldron, Segata, "Machine Learning Meta-analysis of Large Metagenomic Datasets: Tools and Biological Insights", PLoS Comput Biol 2016 (https://doi.org/10.1371/journal.pcbi.1004977, read on PMC4939962; https://github.com/segatalab/metaml). As published in MetAML: 232 stool samples (Table 1: 118 cirrhosis, 114 controls; the Methods say "123 patients affected by liver cirrhosis and 114 healthy controls") x 288,347 binary presences of species- and strain-specific markers, the species abundances being the other profile; TabBench-Bio keeps markers present in at least 10% of the training rows (33,539). Year 2014 for the samples, 2016 for the profiles: left empty for the curator (PROV-9).
- Use case: a clinician screening for cirrhosis with a stool test; the source names the aim ("On the basis of only 15 biomarkers, a highly accurate patient discrimination index is created and validated on an independent cohort. Thus microbiota-targeted biomarkers may be a powerful tool for diagnosis of different diseases", abstract); fit approximate (hospital patients against healthy people, while cirrhosis is diagnosed by imaging, elastography or biopsy); regime IID, one stool sample per person (USE-11); Qin's discovery cohort (98 patients, 83 controls) and validation cohort are a split the source prescribes, a claim (SPLIT-5).
- Siblings and duplicates: `gut_microbiome_liver_cirrhosis` (from the curator's Zotero collection) is the same cohort and target from the same MetAML package with the species abundances: a processing variant, so one of the two enters and the curator picks (PROV-6); MetAML found marker-based predictions "slightly better but overall consistent" (Results). `gmrepo_gut_microbiome_disease`, `meta2db_microbiome_disease_state` and `phlame_colorectal_cancer_metagenome` are larger multi-cohort microbiome sources; whether they hold Qin's cohort is not checked. `cirrhosis_patient_survival_prediction` and `pbcseq` are clinical PBC data, unrelated. External collections: TabBench-Bio (arXiv 2609.07441, Table 4, `gut-cirrhosis`), MetAML; curatedMetagenomicData per the sibling record's links.
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Papers and pages: Qin et al. 2014; Pasolli et al. 2016 (MetAML); comments on Qin et al. in Nature 525:E1-E3 (2015), not read.
- Metric: MetAML's one stated criterion, with its reason: "Prediction performance was evaluated by the area under the curve (AUC) metric, which summarizes true positive and false positive rates and is robust to unequal proportions of each outcome" (Results, "Cross-validation studies revealed good capabilities for disease prediction"), so `roc_auc` (MET-5), which is also the fallback. Inputs none.
- Risks for /add-dataset: the duplicate with `gut_microbiome_liver_cirrhosis` (PROV-6); case-control recruitment (`Selection Bias`); 118 against 123 cases between MetAML's table and text; 288k sparse binary columns, with any prevalence filter fit inside the training folds (LEAK-31), as TabBench-Bio does; one hospital in Hangzhou; 232 rows (`Tiny Data`).
- Priority: gap 0 (medical 44, binary not thin), use case 0 (approximate), source + (Nature paper and MetAML), shape 0 (232 rows), risk - (a processing variant of `gut_microbiome_liver_cirrhosis`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 232 x 33,539 (raw 288,347 binary markers; >=10% prevalence filter on training rows); target: disease (118 cases / 114 controls).
- Why: Liver cirrhosis vs healthy control from stool metagenome strain-marker presence (Qin et al. 2014 cohort as packaged in MetAML, Pasolli et al. 2016)
- Notes: One stool sample per subject; CV grouped by participant. Existing cirrhosis records (cirrhosis_patient_survival_prediction, pbcseq) are clinical PBC data, not this task.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same samples and target (`gut_microbiome_liver_cirrhosis`; PROV-6). The curator keeps one, or both as distinct tasks.
