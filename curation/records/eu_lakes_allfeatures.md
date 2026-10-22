---
unique_name: eu_lakes_allfeatures
name: eu_lakes_allfeatures
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Tiny Data
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2012'
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
original_data_state: One Table
source_row: 874
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3): a microbial-ecology survey table: the study relates bacterial abundances to lake chemistry and geography and predicts nothing, and no target is defined for this record.
- Source: the August 2012 sampling of European lakes by Jens Boenigk's group: metadata from Molecular Ecology (doi:10.1111/mec.15872), OTU table "from J. Boenigk"; the record's reference, Nuy, Hoetzinger, Hahn, Beisser and Boenigk 2020, "Ecological Differentiation in Two Major Freshwater Bacterial Taxa Along Environmental Gradients", Frontiers in Microbiology 11:154: "Sampling of 255 European freshwater lakes was conducted in August 2012", one sample per lake. As published: an OTU (16S V2-V3) abundance matrix plus pH, temperature, conductivity, lake area, elevation, latitude and longitude.
- Use case: none: the paper's responses are OTU and subcluster abundances and diversity indices, explained by the abiotic factors through variation partitioning and rank correlations; no machine learning, no prediction. A target of our own (lake pH from the community) would be a task the source never posed (SEL-8), on about 255 rows with thousands of OTU columns.
- Siblings and duplicates: `eu_lakes_allsamples` (the same sampling, another cut; `TBD -> 2nd Tier`, AI), and the other environmental OTU records of the same import (`bog_lakes` `No` by an AI, `tara_oceans`, `nz_springs`, `bedford_basin_*`, `subseafloor_arc*`), to be treated alike. External collections: none found.
- Metric: none found (the paper fits no model).
- Reject check (AI, 2026-10-22): stands. The microbiome family does have a collection: Zschaubitz, ..., Sperlea 2025, 'A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets', CSBJ (doi 10.1016/j.csbj.2025.04.017, https://pmc.ncbi.nlm.nih.gov/articles/PMC12049816/), Table 1, with targets fixed per dataset; but its Methods say 'The choice of target variable was based on an expectation that there is a correlation': chosen to benchmark feature selection, not for a decision, and the first source is a discovery study (SEL-8). Here the target is Mg (86 samples; eu_lakes_allsamples uses pH, 232 samples), measured in the same lake survey; Nuy et al. 2020 (https://www.frontiersin.org/article/10.3389/fmicb.2020.00154/full) fits no predictive model. Treat it the same as eu_lakes_allsamples, nz_springs, ports, subseafloor_*, tara_oceans (currently AI TBD -> 2nd Tier): same collection, same reasoning.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

A 2012 sampling of European lakes with a microbiome OTU (operational taxonomic unit) abundance table plus metadata. It is already tagged 'Tiny Data' and 'Many features', i.e. a wide, low-sample-count omics matrix that is poorly representative of typical tabular ML and likely too small for stable CV. The intended supervised target is unclear from the record (some lake/sample property to be regressed or classified). A human must identify a concrete target, confirm the (small) sample count and feature count, and judge whether the high-dimensional microbiome data is suitable at all.

---

Sampling of European lakes in August 2012; metadata source: dx.doi.org/10.1111/mec.15872; otu table source: from J. Boenigk

## Reference

10.3389/fmicb.2020.00154
