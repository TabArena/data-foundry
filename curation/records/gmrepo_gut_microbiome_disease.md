---
unique_name: gmrepo_gut_microbiome_disease
name: 'GMrepo v3: curated human gut metagenomes with disease phenotypes'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Website
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://gmrepo.humangut.info
- https://doi.org/10.1093/nar/gkaf1190
- https://doi.org/10.1093/nar/gkab1019
- https://evolgeniusteam.github.io/gmrepodocumentation/usage/downloaddatafromgmrepo/
- https://doi.org/10.64898/2026.03.01.708821
- https://doi.org/10.1093/nar/gkz764
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: GMrepo v3, a curated repository of 118,965 human gut microbiome runs from 890 projects (87,048 16S, 31,917 shotgun) with reprocessed species and genus abundances and 302 phenotypes; a real source for stool-based disease classification, but a database rather than a task: the phenotype, the cohorts and the sequencing type are to choose, and cases and controls often come from different projects.
- Source: GMrepo, a curated human gut metagenome database: v1 NAR (2020, online 2019, https://doi.org/10.1093/nar/gkz764, not read); v2 Dai et al., NAR 50(D1) (2022, https://doi.org/10.1093/nar/gkab1019; 353 projects, 71,642 samples per the v3 paper); v3 Liu et al., NAR 54(D1):D734-D742 (2026, online 2025-11-24, https://doi.org/10.1093/nar/gkaf1190): 890 projects, 118,965 runs (87,048 16S rRNA, 31,917 metagenomic), annotated diseases up from 133 to 302 (from a search summary of the abstract; full text not read). As published (the download documentation): run and sample metadata with the project, run-to-phenotype links (a run can carry several), relative abundances at species and genus level for the runs that pass QC, project tables, a full MySQL dump and a REST API; raw reads stay at SRA. Year left empty: 2019 for v1, 2025 for v3 (PROV-9, for the curator).
- Use case: a clinician screening for a disease from a stool sample, as the cohort studies do; GMrepo itself names marker discovery and cross-dataset comparison, not a decision; fit approximate (case-control cohorts). Peng and Abeel (bioRxiv 2026, https://doi.org/10.64898/2026.03.01.708821, abstract read) meta-trained on 52 GMrepo v2 cohorts and tested few-shot on five diseases. Regime grouped by project (study, country, sequencing protocol), never a pooled IID split.
- Siblings and duplicates: `gut_microbiome_liver_cirrhosis` and `gut_cirrhosis_metaml` (one Qin et al. 2014 cohort, MetAML and curatedMetagenomicData profiles), `meta2db_microbiome_disease_state` and `phlame_colorectal_cancer_metagenome` (unscreened) are single cohorts or other compilations of the same kind; GMrepo likely holds some of the same runs reprocessed, so one source per disease task (PROV-6), to check when a task is chosen. External collections: none in our vocabulary.
- Better data: from the curator's Zotero collection (item 112, the STUNT preprint); no search for better data in this run.
- Papers and pages: the three NAR papers; the GMrepo download documentation; Peng and Abeel 2026.
- Metric: none found for a prediction (the v3 abstract, the download page and the STUNT abstract name none), so the fallback: `roc_auc` for a disease against healthy controls, `log_loss` for a multiclass phenotype (MET-1, MET-8). Inputs: the project, as the group of the split, not a feature.
- Risks for /add-dataset: the task is to define: one disease against healthy controls across its projects, or several phenotypes (`Needs extensive data wrangling`); pooled across projects, phenotype and project are confounded wherever a project holds only cases or only controls, so a model can learn the study (primer region, extraction, country) instead of the disease (`Class-dependent Recording`, LEAK-13 to LEAK-15; and `Selection Bias` of case-control recruitment), to check per task; 16S and shotgun profiles are not comparable and belong in separate tasks; sparse compositional features with thousands of taxa; repeated runs of one subject need a subject group; table joins over the dump or the API.
- Priority: gap 0 (medical and biology are not thin), use case 0 (no decision named), source + (three NAR database papers, maintained), shape + (tens of thousands of runs in hundreds of projects), risk - (the task and cohorts to build, and project confounded with phenotype).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 112: "Evaluating Few-Shot Meta-Learning using STUNT for Microbiome-Based Disease ...".
- as published: v3: 118,965 runs/samples from 890 projects (87,048 16S, 31,917 shotgun; 664 projects with at least one run passing QC), 302 phenotypes (301 diseases plus healthy). Curated metadata (phenotype, age, ...; target: Host phenotype per sample: disease vs healthy control (per project or pooled), or the disease class; access: open.
- Why: The largest uniformly reprocessed and consistently annotated human gut microbiome source, with many disease-vs-control cohorts; the STUNT paper shows they are usable for classification.
- Adds: An alternative and superset source for the microbiome diagnosis tasks proposed elsewhere in this run (meta2db_microbiome_disease_state, phlame_colorectal_cancer_metagenome, phlame_gut_microbiome_health_status, gut_microbiome_liver_cirrhosis): pick one source per task. Access now checked: bulk files and API ...
