---
unique_name: subseafloor_arc
name: subseafloor_arc
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
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
source_row: 861
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3): the Archaea amplicon table of a census of marine-sediment microbial diversity; the source publishes no predictive task and the record names no target.
- Source: Hoshino et al., "Global diversity of microbial communities in marine sediment", PNAS 2020 (https://doi.org/10.1073/pnas.1919139117); as published: 16S amplicon sequence variants (Archaea and Bacteria) from "40 globally distributed sampling locations, spanning sediment depths of 0.1 to 678 m", sample metadata in SI Tables 1 and 2 (PDF); the record's OTU-table link is empty.
- Use case: none; the paper's aim is descriptive ("the global taxonomic diversity ... remain unclear. We investigated microbial composition", Significance), and its finding is which environmental factors explain composition. A target such as oxygen presence or organic carbon is measured on the core, not predicted from sequencing; fit none.
- Siblings and duplicates: `subseafloor_arc_2` is the Bacteria table of the same study (its `name` field also says `subseafloor_arc`); the other microbiome records of this set (`bog_lakes`, `bedford_basin_*`, `boso_fish`, `nz_springs` proposed `No` in this re-screen; `australia`, `atl_ocean_transect`, `wastewater_treatment` `No` (AI)). External collections: none found.
- Metric: none (a discovery study).
- Reject check (AI, 2026-10-22): stands. SEL-3: Hoshino et al., PNAS 2020 (https://doi.org/10.1073/pnas.1919139117, PMID 33077589) abstract: the taxonomic diversity "ha[s] been poorly constrained on a global scale. We investigated 299 globally distributed sediment core samples from 40 different sites ... Statistical analysis reveals significant correlations between taxonomic composition, sedimentary organic carbon concentration, and presence or absence of dissolved oxygen": a census, no prediction a decision uses; oxygen and organic carbon are measured on the core. The record has no target and an empty OTU-table link. Same family call as bog_lakes (reject check stood).
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

A subseafloor microbiome dataset (Archaea) built by joining a PDF-supplement metadata table with an OTU abundance table (PNAS 10.1073/pnas.1919139117). This is a microbiome/metagenomics scientific-discovery dataset with many features and substantial wrangling needed to assemble; whether a clean, deployable tabular target (e.g. an environment/site label) exists is unclear. The microbiome/OTU framing leans toward scientific discovery rather than representative tabular ML. A human must define the target, assess sample size after joining (microbiome studies are often very small), and confirm it is not duplicative of subseafloor_arc_2.

---

Subseafloor microbiome project, Archaea; metadata source: SI Table 1&2 (PDF); otu table source:

## Reference

10.1073/pnas.1919139117
