---
unique_name: gut_microbiome_liver_cirrhosis
name: Gut microbiome liver cirrhosis cohort (Qin et al. 2014; MetAML / curatedMetagenomicData)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://github.com/SegataLab/metaml
- https://arxiv.org/abs/2606.24995
- https://doi.org/10.1038/nature13568
- https://doi.org/10.1371/journal.pcbi.1004977
- https://doi.org/10.1038/nmeth.4468
- https://github.com/waldronlab/curatedMetagenomicData
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: liver cirrhosis against healthy controls from stool species abundances (Qin et al. 2014; 232 people in MetAML and curatedMetagenomicData); a real diagnostic cohort, but tiny with about twice as many taxa as people, case-control, and the same samples and target as `gut_cirrhosis_metaml` (strain markers), so one of the two enters (PROV-6).
- Source: Qin, Yang, Li et al., "Alterations of the human gut microbiome in liver cirrhosis", Nature 513:59-64 (2014), https://doi.org/10.1038/nature13568 (abstract, as read on the sibling record). Species-level profiles: MetAML (Pasolli, Truong, Malik, Waldron, Segata, PLoS Comput Biol 2016, https://doi.org/10.1371/journal.pcbi.1004977) and curatedMetagenomicData (Pasolli et al., Nat Methods 2017, https://doi.org/10.1038/nmeth.4468; MetaPhlAn2 relative abundances through ExperimentHub). As used by Perciballi et al. (arXiv 2606.24995, Sec. 4.1, from ExperimentHub): discovery 178 samples x 520 species (83 control, 95 cirrhosis), validation 54 x 394 (31, 23), "species-level taxa (microbial species relative abundance)". Year left empty, as on the sibling: 2014 for the samples, 2016-2017 for the profiles (PROV-9, for the curator).
- Use case: as on `gut_cirrhosis_metaml`: a stool-based screen for cirrhosis; Qin et al. build "a highly accurate patient discrimination index" on 15 biomarkers, validated on an independent cohort (abstract); fit approximate (hospital patients against healthy people, while cirrhosis is diagnosed by imaging, elastography or biopsy). Regime IID, one stool sample per person (USE-11); Qin's discovery and validation cohorts are a split the source prescribes (SPLIT-5, a claim).
- Siblings and duplicates: `gut_cirrhosis_metaml` (`TBD -> 2nd Tier`, priority 1, screened in this run) holds the same 232 samples and target as MetAML's strain-marker presence (288,347 binary columns; TabBench-Bio): a processing variant, so one of the two enters and the other becomes a `Duplicate` (PROV-6). Species abundances are the profile curatedMetagenomicData and Perciballi et al. use, so this record is the natural one to keep; the curator picks. `gmrepo_gut_microbiome_disease` may hold the same runs reprocessed. The clinical cirrhosis records (`cirrhosis_patient_survival_prediction`, `pbcseq`, `halt_c_hcv_cirrhosis_labs`) are other tasks. External collections: MetAML and curatedMetagenomicData (not in our vocabulary).
- Better data: from the curator's Zotero collection (item 219, arXiv 2606.24995); no search for better data in this run.
- Papers and pages: Qin et al. 2014; Pasolli et al. 2016 and 2017; Perciballi, Fall, Granese, Prifti, Zucker, "Are Tabular Foundation Models Robust to Realistic Query Distribution Shifts in Microbiome Data?" (arXiv 2606.24995, 2026).
- Metric: `roc_auc`. MetAML states it as its criterion with its reason ("robust to unequal proportions of each outcome", Results, quoted on the sibling record), and Perciballi et al. write "Performance is measured by AUROC" (Appendix B); MET-5, and also the fallback. Inputs none.
- Risks for /add-dataset: the PROV-6 pair with `gut_cirrhosis_metaml`; case-control recruitment (`Selection Bias`); 232 rows with about 500 sparse compositional columns (`Tiny Data`, `Many features`); the discovery and validation profiles carry different taxa (520 against 394), so a union filled with zeros; a prevalence filter on taxa is fit inside the training folds (LEAK-31).
- Priority: gap 0 (medical and binary are not thin), use case 0 (approximate), source + (Nature paper and two curated releases), shape 0 (232 rows), risk - (a processing variant of `gut_cirrhosis_metaml`, case-control).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 219: "Are Tabular Foundation Models Robust to Realistic Query Distribution Shifts in ...".
- as published: one stool metagenome per person: 232 samples as used by the paper (discovery 178, 83 control/95 cirrhosis; validation 54, 31/23) x about 520 species relative abundances (MetaPhlAn); Chinese patients ...; target: liver cirrhosis vs healthy control (binary); access: open.
- Why: Real, public, peer-reviewed cohort with a clinical target and a separate validation cohort; in this paper and in MetAML it has the strongest signal of the gut-disease cohorts (AUROC about 0.93)
- Adds: The first human-microbiome diagnosis task; the microbiome records we have are environmental metabarcoding without a target (tara_oceans and siblings). Caveats: very small, with p > n; case-control recruitment (Selection Bias); compositional, zero-inflated features. A larger multi-cohort task (e.g. colorectal cancer) ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same samples and target (`gut_cirrhosis_metaml`; PROV-6). The curator keeps one, or both as distinct tasks.
