---
unique_name: eu_lakes_allsamples
name: eu_lakes_allsamples
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Duplicate
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
source_row: 875
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, `Duplicate`; SEL-3, PROV-6): an OTU table of European lakes published for describing community structure, with no predictive target, and the all-samples cut of the same data as `eu_lakes_allfeatures`.
- Source: Boenigk et al., "Geographic distance and mountain ranges structure freshwater protist communities on a European scale", Metabarcoding and Metagenomics 2 (2018), doi 10.3897/mbmg.2.21519: "eukaryotic ribosomal amplicon diversity from 218 European freshwater lakes sampled in August 2012 to assess the effect of mountain ranges as biogeographic barriers". Metadata from Sperlea et al., Molecular Ecology 2021, doi 10.1111/mec.15872, which presents "a methodological framework to quantify the covariation of the microbial community of a habitat and environmental variables" (more than twenty physicochemical and geographic variables, used to identify bioindicators). OTU table from J. Boenigk (not public as a file). As published: about 218 lakes x thousands of OTUs; no target named.
- Use case: none in the sources; the ML in Sperlea et al. measures explained variance per environmental variable (discovery), not a decision at a prediction point (SEL-3, USE-2).
- Siblings and duplicates: `eu_lakes_allfeatures` is the same study and OTU table (another cut, PROV-6); the other OTU records of this list (`bog_lakes`, `bedford_basin_v4v5`, `bedford_basin_v6v8`, `atl_ocean_transect`) were proposed `No` on the same ground in this re-screen.
- Metric: none (no task in the source).
- Reject check (AI, 2026-10-22): stands. SEL-3 holds on its own: all three papers on this survey are discovery studies. The record's own reference (doi 10.1111/1462-2920.14992, Environmental Microbiology 2020) says 'we address the relative importance of these different factors in shaping protists and bacterial communities on a European scale', and Sperlea et al. (https://doi.org/10.1111/mec.15872) 'quantify the covariation of the microbial community ... and environmental variables'. Its mention of bioindicators 'for lake water monitoring schemes' is about picking indicator taxa, not running a model to make a decision. The PROV-6 cut was not verified (the two records cite different papers), but the reject does not depend on it.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

Companion to eu_lakes_allfeatures: the same 2012 European-lakes microbiome OTU study, here the 'all samples' variant, again tagged 'Tiny Data' and 'Many features'. As a wide, low-sample omics table it is poorly representative of mainstream tabular ML, likely too small, and overlaps heavily with the sibling record (potential duplication of source data). The supervised target is unspecified. A human must define the target, confirm size/dimensionality, and decide whether to keep this or the features variant (or neither).

---

Sampling of European lakes in August 2012; metadata source: dx.doi.org/10.1111/mec.15872; otu table source: from J. Boenigk

## Reference

10.3897/mbmg.2.21519 ; 10.1111/1462-2920.14992
