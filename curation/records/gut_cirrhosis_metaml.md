---
unique_name: gut_cirrhosis_metaml
name: gut-cirrhosis (Gut microbiome markers, healthy vs cirrhosis)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Many features
- Tiny Data
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- TabBench-Bio
collection_period: '2011'
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 1: liver cirrhosis against healthy controls from stool strain-marker presence (the Qin et al. 2014 cohort as packaged by MetAML); a real diagnostic aim with its label from a separate work-up, but the same 232 samples and target as `gut_microbiome_liver_cirrhosis`, which uses the species abundances (PROV-6), case-control and tiny.
- Source: Qin, Yang, Li et al., "Alterations of the human gut microbiome in liver cirrhosis", Nature 513:59-64, online 2014-07-23 (https://doi.org/10.1038/nature13568; reads in ENA PRJEB6337, first public 2014-06-13); packaged by MetAML: Pasolli, Truong, Malik, Waldron, Segata, PLoS Comput Biol 2016 (https://doi.org/10.1371/journal.pcbi.1004977; https://github.com/segatalab/metaml). As published in MetAML: 232 stool samples (Table 1: 118 cirrhosis, 114 controls; the Methods say 123 patients) x 288,347 binary presences of species- and strain-specific markers, the species abundances being the other profile; TabBench-Bio keeps markers present in at least 10% of the training rows (registry `gut-cirrhosis`, read 2026-11-25: "Qin cirrhosis cohort in MetAML: 118 cases and 114 controls, all stool, 232 distinct subjects. Participant-grouped CV"). Year 2014 for the samples, 2016 for the profiles: left empty for the curator (PROV-9).
- Use case: a clinician screening for cirrhosis with a stool test; the source names the aim ("On the basis of only 15 biomarkers, a highly accurate patient discrimination index is created and validated on an independent cohort. Thus microbiota-targeted biomarkers may be a powerful tool for diagnosis of different diseases", abstract); fit approximate (hospital patients, about 65-76% decompensated, against healthy people, while cirrhosis is diagnosed by imaging, elastography or biopsy); the label comes from that separate work-up, so it is ground truth (USE-1). Collection: patients and controls recruited over time, one stool sample per person, the diagnosis with the sample; ENA gives `collection_date` 2011 for all 314 runs, and the sample aliases name only cohort and group (HD 83, LD 98 in discovery; HV 31, LV 25 in validation), so no per-row date or arrival order: samples over time, time lost; type `Clinical Study`.
- Split: leaf L-FORCED.random (`ForcedIIDFromTemporal`) because [CLI.meets] later patients at the same clinic (the source names no other hospital), [CLI.dated] no (one year for every run), [ORDER.order] no (aliases number patients within each group, not by arrival), [FORCED.test] nothing measurable, [FORCED.reason] and [FORCED.risk] no until a person answers, [FORCED.groups] no (one sample per person, no periods); open: whether the validation cohort was recruited after the discovery cohort (then two periods to test at [FORCED.test]); `AssumedStationaryRelation` for a person (for: a physiological signal read against a clinical diagnosis; against: a hospital's case mix and the sequencing change); the discovery and validation cohorts are a split the source used, a claim (SPLIT-5).
- Siblings and duplicates: `gut_microbiome_liver_cirrhosis` (`TBD -> 2nd Tier`, priority 1) is the same cohort and target from the same MetAML package with the species abundances: a processing variant, so one of the two enters and the curator picks (PROV-6); species abundances are what curatedMetagenomicData and Perciballi et al. (arXiv 2606.24995) use, and MetAML found marker-based predictions "slightly better but overall consistent" (Results). `gmrepo_gut_microbiome_disease`, `meta2db_microbiome_disease_state` and `phlame_colorectal_cancer_metagenome` are larger multi-cohort microbiome sources; whether they hold Qin's cohort is not checked. `cirrhosis_patient_survival_prediction` and `pbcseq` are clinical PBC data, unrelated. External collections: TabBench-Bio (arXiv 2609.07441, Table 4, `gut-cirrhosis`), MetAML, curatedMetagenomicData.
- Better data: none found in a quick look (web search for larger shotgun cirrhosis cohorts: Loomba et al.'s NAFLD-cirrhosis cohort of 27 patients and 54 controls, Wei et al. 2018 with 47 controls and 95 patients, a 2025 HBV-cirrhosis study in northwest China; none larger); the 2026-10-31 run searched no further.
- Papers and pages: Qin et al. 2014; Pasolli et al. 2016 (MetAML); Bajaj et al.'s comment on the cohorts' decompensation share; Perciballi et al. 2026.
- Metric: MetAML's one stated criterion, with its reason: "Prediction performance was evaluated by the area under the curve (AUC) metric, which summarizes true positive and false positive rates and is robust to unequal proportions of each outcome" (Results), so `roc_auc` (MET-5), which is also the fallback. Inputs none.
- Risks for /add-dataset: the duplicate with `gut_microbiome_liver_cirrhosis` (PROV-6); case-control recruitment (`Selection Bias`); 118 against 123 cases between MetAML's table and text; 288k sparse binary columns, with any prevalence filter fit inside the training folds (LEAK-31), as TabBench-Bio does; one hospital in Hangzhou; 232 rows (`Tiny Data`); the forced split goes to a reviewer.
- Priority: gap 0 (medical 39, binary 86, none thin), use case 0 (approximate), source + (Nature paper and MetAML), shape 0 (232 rows), risk - (a processing variant of `gut_microbiome_liver_cirrhosis`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 232 x 33,539 (raw 288,347 binary markers; >=10% prevalence filter on training rows); target: disease (118 cases / 114 controls).
- Why: Liver cirrhosis vs healthy control from stool metagenome strain-marker presence (Qin et al. 2014 cohort as packaged in MetAML, Pasolli et al. 2016)
- Notes: One stool sample per subject; CV grouped by participant. Existing cirrhosis records (cirrhosis_patient_survival_prediction, pbcseq) are clinical PBC data, not this task.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same samples and target (`gut_microbiome_liver_cirrhosis`; PROV-6). The curator keeps one, or both as distinct tasks.
