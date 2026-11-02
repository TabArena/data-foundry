---
unique_name: tara_oceans
name: tara_oceans
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_row: 863
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): taxonomic profiles of Tara Oceans samples joined to their metadata, published to describe ocean-microbiome structure and its ecological determinants; no predictive task, no target in the record.
- Source: Sunagawa et al., "Structure and function of the global ocean microbiome", Science 2015 (https://doi.org/10.1126/science.1261359); companion site http://ocean-microbiome.embl.de/companion.html (Tables W1 and W8, miTAG.taxonomic.profiles.release.tsv); 243 samples from 68 locations, 139 prokaryote-enriched.
- Use case: none; the abstract's aim is "a global picture of ... microbial community structure, and their ecological determinants". Depth, temperature or region are measured at sampling, not predicted from sequencing; fit none. About 140-240 samples would also be small.
- Siblings and duplicates: the microbiome set (`subseafloor_arc`, `subseafloor_arc_2`, `bog_lakes`, `bedford_basin_*`, `boso_fish`, `nz_springs` proposed `No` in this re-screen; `australia`, `atl_ocean_transect` `No` (AI)). External collections: none found.
- Metric: none (a discovery study).
- Reject check (AI, 2026-10-22): stands. SEL-3: Sunagawa et al., Science 2015 (https://doi.org/10.1126/science.1261359, PMID 25999513), "Structure and function of the global ocean microbiome": a description of community structure and its drivers ("epipelagic community composition mostly driven by temperature"); no prediction a decision uses, depth/temperature/region are measured at sampling, and the record names no target. Same family call as bog_lakes.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

The Tara Oceans marine microbiome dataset (Science 10.1126/science.1261359), assembled by joining companion-website metadata tables (W1/W8) with a 16S OTU abundance table. As with the subseafloor records, this is a metagenomics/microbiome scientific-discovery resource with many features and heavy wrangling; the existence of a clean, deployable tabular target and adequate sample size is uncertain. The OTU/microbiome framing tends toward scientific discovery rather than representative tabular ML. A human must define a target (e.g. ocean region/depth/biome), check post-join sample size, and confirm it is not better treated as discovery.

---

World-wide sampling cruise; metadata source: http://ocean-microbiome.embl.de/companion.html ("Companion Website Tables/Tables W1-W8 (.xlsx)" -- table W1 and W8); otu table source:http://ocean-microbiome.embl.de/companion.html ("16S OTU table (*.tsv.gz)" / miTAG.taxonomic.profiles.release.tsv)

## Reference

10.1126/science.1261359
