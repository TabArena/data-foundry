---
unique_name: cryptic_mtb_drug_resistance
name: 'CRyPTIC data compendium: genomes and resistance phenotypes of 12,289 Mycobacterium tuberculosis isolates'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '? (2021)'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/
- https://doi.org/10.1371/journal.pbio.3001721
- https://arxiv.org/abs/2509.25216
- https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 12,289 Mycobacterium tuberculosis isolates from 23 countries with whole genomes and MIC-based resistance to 13 drugs, an open consortium release for WGS-based resistance prediction; the feature matrix has to be built from the variant calls, and catalogued mutations may nearly decide the first-line drugs.
- Source: The CRyPTIC Consortium, "A data compendium associating the genomes of 12,289 Mycobacterium tuberculosis isolates with quantitative resistance phenotypes to 13 antibiotics", PLoS Biol 20(8):e3001721 (2022; preprint bioRxiv 10.1101/2021.09.14.460274, which the release README asks to cite); data on the EBI FTP (`release_june2022/`: `reuse/` with `CRyPTIC_reuse_table_*.csv` from 2021-10 to 2024-09-17 and a CHANGELOG, `reproducibility/`, `pubs/`). As published: 12,289 isolates with matched genotypes and phenotypes out of 15,211 collected in 23 countries (Results, "The data compendium"); MICs on UKMYC plates with "5 to 10 doubling dilutions of 13 antibiotics" (Methods), read after 14 days by an expert (Vizion), by AMyGDA software and by BashTheBug volunteers, quality HIGH when at least two methods agree; binary R/S from ECOFFs. Reuse table (README): `UNIQUEID`, per drug `XYZ_BINARY_PHENOTYPE`, `XYZ_MIC`, `XYZ_PHENOTYPE_QUALITY`, `ENA_SAMPLE`, `VCF` and `JOINT_GENOTYPED_VCF` paths; GENOTYPES, VARIANTS, MUTATIONS, SAMPLES and PHENOTYPES tables in the reproducibility set (Fig 1 legend). The paper calls the compendium "fully open source" (abstract).
- Use case: a TB reference laboratory, once an isolate is sequenced, predicts its resistance to a drug to choose the regimen before culture-based testing returns; the paper presents the data as a resource "to accelerate antimicrobial resistance (AMR) diagnostic development" and for "mutation catalogues for WGS resistance prediction" (Introduction), and lists "training machine learning models that can predict resistance" (Discussion); fit direct for one drug as a binary task; regime IID or grouped by collection site or country (lineage and site structure, SPLIT-29), for the add stage.
- Siblings and duplicates: `driams_antimicrobial_resistance` (resistance from MALDI-TOF spectra), `amr_uti_antibiotic_resistance` (resistance from health records), `mycobacterium_tuberculosis_drug_data` (`No`, a Kaggle drug-discovery table), `treats_tb_crp_screening` and `treats_tb_prevalence_survey` (screening people for TB): other sources and tasks. No other record of CRyPTIC (grep: cryptic, tuberculosis). External collections: none found.
- Better data: from the curator's Zotero collection (item 11); no further search this round.
- Papers and pages: the compendium paper; the consortium's GWAS and ECOFF papers in `pubs/` (not read); Comesaña Cimadevila, "Evaluating Double Descent in Machine Learning: Insights from Tree-Based Models Applied to a Genomic Prediction Task", arXiv 2509.25216 (2025), isoniazid resistance from WGS (the Zotero item; its abstract does not name the dataset).
- Metric: the paper scores a mutation catalogue's hard calls by sensitivity and specificity (Results, "Genetic-based predictions of resistance"), several threshold metrics with no fixed cost: the fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none. An MIC regression would need its own metric (agreement within one dilution), not declared here.
- Risks for /add-dataset: a feature matrix must be built from the VCFs or the MUTATIONS table (candidate genes or genome-wide; wide and sparse; `Needs extensive data wrangling`); 13 drugs: one target per dataset (CLEAN-18); rifampicin and isoniazid resistance are largely explained by a few catalogued mutations, so probe a catalogue rule (TP-4) and prefer a drug where the catalogue falls short; LOW-quality phenotypes (filter or keep, USE-5); the compendium is enriched for resistance and "not suitable for measuring prevalence" (Introduction), which changes the class shares only (no `Selection Bias` marker); several reuse-table versions (take the latest, read the CHANGELOG); 12,288 vs 12,289 isolates between sections of the paper.
- Priority: gap 0 (medical and biology, binary not thin), use case + (the paper names WGS resistance prediction for diagnostics), source + (a consortium paper and the EBI release with a README), shape + (12,289 isolates, genomic features), risk - (a heavy feature build; a catalogue rule may nearly decide the first-line drugs).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 11: "Evaluating Double Descent in Machine Learning: Insights from Tree-Based Models Applied ...".
- as published: 12,289 isolates from 23 countries; binary phenotype, MIC and phenotype quality for 13 drugs (reuse table); variant calls as per-sample and joint-genotyped VCFs and a MUTATIONS table in ...; target: resistant vs susceptible to a drug (e.g. isoniazid, rifampicin), or the MIC as regression; access: open.
- Why: real, large, open, an established clinical task (WGS-based drug susceptibility prediction); phenotypes measured on a standard 96-well MIC plate with a quality flag
- Adds: genomic antimicrobial-resistance domain; needs a feature matrix built from the mutations (extensive wrangling), high-dimensional and sparse; lineage or country as groups; check the WHO-catalogue rule baseline for triviality (TP-4)
