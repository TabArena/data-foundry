---
unique_name: meta2db_microbiome_disease_state
name: 'Meta2DB: curated shotgun metagenomic feature sets and metadata for health state prediction'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Many features
original_source: Other
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zenodo.org/records/17315984
- https://doi.org/10.1093/bioinformatics/btag422
- https://doi.org/10.1101/2024.10.03.616398
- https://gdo-meta2db.llnl.gov
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Meta2DB, 13,897 public human shotgun metagenomes from 84 studies reprocessed by one LLNL pipeline into taxonomy count tables with curated host metadata, for health-state prediction; real and documented, but the pooled "any disease against control" label fits no decision, case and control status is tied to the study, and the same public runs sit in GMrepo and the single-cohort records.
- Source: Kok, Mulakken, Thissen, Martí, Lee, Trainer et al., "Meta2DB: curated shotgun metagenomic feature sets and metadata for health state prediction", bioRxiv (2024-10-04, https://doi.org/10.1101/2024.10.03.616398), Bioinformatics (2026, https://doi.org/10.1093/bioinformatics/btag422); Zenodo record 17315984 (2025-10-13, CC BY 4.0) and https://gdo-meta2db.llnl.gov. Abstract: "structurally consistent microbiome taxonomy feature count tables for 13 897 samples across 84 studies, 23 disease states, and 34 geographical locations", with metadata "specifically structured to facilitate training of ML models for prediction of human health". As published (Zenodo API and a header preview): profile tables (421 MB zip), a lineage file, `meta2db_metadata.csv` (52 MB) with study fields (`project_name`, `pub_date`, `pub_abstract`), sample and sequencing fields, `health_disease_stat`, `host_disease_stat`, `disease_category` and per-organ disorder fields, host age, sex, BMI, body site, `host_subject_id`, `visit_number`, and disease-specific clinical columns (MELD, AJCC stage, HbA1c and many more); study names follow curatedMetagenomicData (for example `2013_KarlssonFH`).
- Use case: a per-disease screen (a clinician tests a stool sample for colorectal cancer) is a real decision; the source's pooled health state across 23 diseases and several body sites names no actor. Fit approximate. Regime grouped by study (a new cohort or lab), with samples of one subject kept together (SPLIT-3, SPLIT-24).
- Siblings and duplicates: `gmrepo_gut_microbiome_disease` (unscreened; GMrepo v3, reprocessed gut metagenomes with phenotypes, a superset of many of the same studies), `gut_microbiome_liver_cirrhosis` (unscreened; Qin et al. 2014, a curatedMetagenomicData study likely inside Meta2DB), `gut_cirrhosis_metaml` (`TBD -> 2nd Tier`, priority 1), `phlame_colorectal_cancer_metagenome` (unscreened; colorectal cancer studies): other processings of the same public runs, so one source per task (PROV-6 to settle); `mgnify_hmp_isolation_source` and `bog_lakes` (`No`, no target). External collections: none found.
- Better data: from the curator's Zotero collection (items 18 and 171; the same record as hits of two other batches); no further search this round.
- Papers and pages: the Bioinformatics note; the embeddings paper (Valdes et al., "An Embeddings Fusion Approach Predicts Disease State from Microbiome Features", bioRxiv 2026, https://doi.org/10.64898/2026.04.20.719747, abstract: "Our model achieves an average classification performance of 84% in distinguishing healthy and disease conditions; 87% for disease types, 99% for body sites, and 88% for geographical locations") and its code (https://github.com/LLNL/invisorg), both moved here from the source links (PROV-12).
- Metric: none found as a deliberate choice (the data paper defines no evaluation; the embeddings paper's headline is an accuracy-like percentage), so the fallback `roc_auc`, `log_loss` for a disease-type framing (MET-5, MET-8). Inputs: none.
- Risks for /add-dataset: study-confounded labels (studies that bring mostly cases or mostly controls, each with its own protocol, to count; `Class-dependent Recording`, LEAK-13 to LEAK-15; the 99% body-site and 88% geography scores show strong study signals); drop the study and disease fields (`project_name`, `experimental_factor`, `pub_abstract`, `disease_category`, disorder fields, disease-specific clinical columns; LEAK-10); repeat samples per subject (SPLIT-29); the overlap with GMrepo and the single-cohort records (PROV-6); tens of thousands of sparse taxa (`Many features`; CLEAN-22: width is no reason to drop).
- Priority: gap 0 (medical binary tasks are well covered), use case 0 (pooled label, no decision named), source + (a peer-reviewed data note, Zenodo with field definitions), shape + (13,897 samples, 84 study groups), risk - (study-confounded labels; overlapping sources).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 171: "An Embeddings Fusion Approach Predicts Disease State from Microbiome Features | bioRxiv"; the curator's Zotero collection, item 18: "Beyond Microbial Abundance: Metadata Integration Enhances Disease Prediction in Human ...".
- as published: 13,897 human shotgun metagenomes from 84 public studies, 23 disease states, 34 countries; taxonomy count tables in a 421 MB zip plus meta2db_metadata.csv (52 MB) and field definitions; target: Host health state (control vs diseased); disease type as a multiclass alternative; access: open.
- Why: Real sequencing counts processed through one pipeline, with curated labels, open under CC BY 4.0. | real measured sequencing-derived counts processed through one pipeline, with a genuine diagnostic target and curated host metadata - unlike the environmental OTU records we rejected (bog_lakes etc.), which have no target
- Adds: Same dataset as zotero_02's and zotero_27's hit meta2db_microbiome_disease_state; confirmed unchanged. Caveats: tens of thousands of taxa (Many features); case/control labels per source study, so study effects are confounded with labels. | a large multi-study human-microbiome classification task with grouped splits ...
