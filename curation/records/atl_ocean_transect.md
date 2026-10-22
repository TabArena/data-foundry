---
unique_name: atl_ocean_transect
name: atl_ocean_transect
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Tiny Data
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
problem_type: Other
original_data_state: Other
source_row: 873
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3): an OTU abundance table from a study of marine bacterial diversity patterns; no predictive task in the source and no target in the record.
- Source: Milici et al., "Low diversity of planktonic bacteria in the tropical ocean", Scientific Reports 6:19054, 2016 (doi 10.1038/srep19054); as published: 16S V5-V6 OTU table and station metadata in the SI, 26 stations x 5 depths x 3 size fractions = 359 samples.
- Use case: none stated; the paper's aim is a discovery ("revealed a clear biogeographic pattern with a double inverted latitudinal gradient"). A framing "predict an environmental variable from the community" would be ours, not the source's (SEL-8), and the variables (temperature, depth) are measured directly at sampling.
- Siblings and duplicates: the microbiome group of records with "metadata source / otu table source" notes (australia, bedford_basin_v4v5, bedford_basin_v6v8, bog_lakes, boso_fish, wastewater_treatment: AI `No`; eu_lakes_allfeatures, eu_lakes_allsamples, nz_springs, ports, subseafloor_arc, subseafloor_arc_2, tara_oceans: AI `TBD -> 2nd Tier`; none verified by a curator). The collection that gathered them is not identified; the closest ML use (Sperlea et al. 2021, Mol Ecol, on EU lakes) quantifies "covariation", also a discovery framing.
- Metric: none (no task).
- Doubt for the reject-checker: environmental-DNA monitoring does predict water-quality indicators from metabarcoding (Bell et al. 2026, bioRxiv, Baltic Sea), so a target could be defined for some siblings; nothing ties this table to such a task.
- Reject check (AI, 2026-10-22): stands. The microbiome family does have a collection: Zschaubitz, ..., Sperlea 2025, 'A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets', CSBJ (doi 10.1016/j.csbj.2025.04.017, https://pmc.ncbi.nlm.nih.gov/articles/PMC12049816/), Table 1, with targets fixed per dataset; but its Methods say 'The choice of target variable was based on an expectation that there is a correlation': chosen to benchmark feature selection, not for a decision, and the first source is a discovery study (SEL-8). Here the target is sampling depth (regression and classification, 113 samples), which is recorded when the sample is taken; no actor predicts it. First source Milici et al. 2016 (https://www.nature.com/articles/srep19054): 'revealed a clear biogeographic pattern'. Correct the block: a target exists in the collection, but it serves no decision.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

An Atlantic Ocean transect microbiome study (26 stations, 5 depths, 3 size fractions) with an OTU abundance table from a paper's supplementary information. This is a microbial-ecology OTU matrix for scientific discovery, not a real-world predictive ML task with a clear target, and it is extremely small (already tagged 'Tiny Data'). High-dimensional OTU tables with tens of samples are not representative of tabular ML and lack a well-posed target. Excluded; a human could confirm sample count but the small size and discovery framing are decisive.

**Update (policy):** removed the "Too Small" marker — size is not a rejection reason (decided post-Data Foundry); this record stays No on its other ground(s).

---

Atlantic Ocean transect spanning 12,000 km; 26 stations, 5 depths, and three size fractions; metadata source: SI of the paper; otu table source: SI of the paper

## Reference

10.1038/srep19054
