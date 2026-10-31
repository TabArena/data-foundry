---
unique_name: phlame_colorectal_cancer_metagenome
name: PHLAME colorectal cancer task (gut metagenome)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
original_source: Other
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://phlame.yassourlab.com/tasks/
- https://doi.org/10.1101/2025.06.12.658885
- https://github.com/yassourlab/phlame-baselines
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: colorectal cancer against healthy controls from stool metagenomes (MetaPhlAn4 species abundances) of about 1,000 people from eight cohorts in seven countries, tested on an independent German cohort (PHLAME); a real non-invasive screening aim with a cross-cohort test, but case-control cohorts, wide compositional features and other records that likely hold the same cohorts.
- Source: the samples come from published case-control cohorts (the preprint's references: Zeller (France), Feng (Austria), Yu (China), Vogtmann (USA), Yachida and Thomas (Japan), Thomas (Italy), Gupta (India); test set Wirbel et al. 2019, Germany), reprocessed by PHLAME: Barak, Bhattacharya, Asnicar, Sung, Segata and Yassour, "PHLAME: A benchmark for continuous evaluation of host phenotype prediction from shotgun metagenomic data", bioRxiv 2025-06-15 (doi 10.1101/2025.06.12.658885); site phlame.yassourlab.com (the task page now names the benchmark CAMPP). As published: training 983 samples (498 CRC, 485 controls, 7 countries) on the site, 1,063 (538 and 525, eight studies) in the preprint; test 125 samples "collected independently in Germany"; "one sample per individual"; "Species-level Taxonomic profiles were generated using MetaPhlAn4"; `crc.zip` on the task page, plus a script to rebuild from the raw reads.
- Use case: a clinician or screening programme triages people for colonoscopy from a stool test (the preprint: "This task aims to reflect a common use case in which researchers demonstrate the application of host phenotype prediction for disease diagnosis"); fit approximate, since the cohorts recruited cases and controls apart (`Selection Bias` to weigh). Regime grouped by study: the test cohort comes from a study absent from training (SPLIT-19 for the prescribed test set).
- Siblings and duplicates: `gmrepo_gut_microbiome_disease` and `meta2db_microbiome_disease_state` (multi-study compilations, unscreened) likely hold the same CRC cohorts, and `gmrepo_gut_microbiome_disease` asks to pick one source per task; `gut_microbiome_liver_cirrhosis` and `gut_cirrhosis_metaml` are cirrhosis tasks of another cohort; the environmental microbiome records have no host phenotype. External collections: PHLAME (CAMPP); curatedMetagenomicData likely carries the cohorts (not checked).
- Better data: from the curator's Zotero collection, item 73; no new search this run.
- Papers and pages: the PHLAME preprint (full text read up to the references) and its task page; the cohort papers were not read.
- Metric: the preprint reports ROC AUC, PR AUC, balanced accuracy, precision, recall and F1 per task and ranks tools overall by a harmonic mean across tasks; no single per-task criterion, so the fallback `roc_auc` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: which source to build from (PHLAME's profiles, or a compilation over the same cohorts; PROV-6 against the two compilations above); the training count differs between the site (983) and the preprint (1,063); hundreds of sparse, compositional species columns; study effects (DNA extraction, sequencing depth) make the grouped split decisive (SPLIT-29); the prescribed test is one cohort of 125, so a split grouped over all nine studies is the alternative.
- Priority: gap 0 (medical & healthcare, binary and grouped are not thin), use case 0 (approximate: case-control cohorts, a research framing), source + (a benchmark preprint over published cohorts), shape + (about 1,100 samples in nine studies, grouped), risk - (the same cohorts likely in two other records).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 73: "PHLAME: A benchmark for continuous evaluation of host phenotype prediction from shotgun ...".
- as published: stool metagenomes: 983 train samples (one per person, 8 studies, 7 countries; the preprint says 1,063) + 125 test (Germany); MetaPhlAn4 species-level relative abundances (wide) or HUMAnN3 pathways; target: colorectal cancer vs healthy control; access: open.
- Why: real case-control cohorts with a prescribed cross-cohort test set (grouped regime) and a clear clinical decision | the largest PHLAME task; study-grouped train and test
- Adds: host-phenotype prediction from microbiome data; the only microbiome tables in the records are environmental ones rejected as No Good Target | a large, wide microbiome classification task with a natural grouped split by study
