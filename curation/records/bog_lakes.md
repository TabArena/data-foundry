---
unique_name: bog_lakes
name: bog_lakes
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
problem_type: Other
original_data_state: Database (or multiple to-be-joined tables)
source_row: 858
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3): the North Temperate Lakes bog-lake 16S OTU table (R package OTUtable) is published to describe bacterial community composition over five years, not for a prediction; no target is named.
- Source: Linz, Crary, Shade, Owens, Gilbert, Knight and McMahon, "Bacterial Community Composition and Dynamics Spanning Five Years in Freshwater Bog Lakes", mSphere 2017, doi 10.1128/mSphere.00169-17 (PMC5489657); 1,387 16S amplicon samples from eight lakes and two thermal layers near Minocqua, Wisconsin; data and scripts in the R package OTUtable (https://amlinz.r-universe.dev/OTUtable) and the McMahon Lab GitHub repository.
- Use case: none; the paper reports year-to-year shifts, a core community and lake-specific communities; any target (lake, layer, year from the OTUs) would be our own and partly a look back at the sampling design (USE-1, USE-2).
- Siblings and duplicates: the other microbiome records of the same import (all AI-screened). External collections: none found.
- Metric: none.
- Reject check (AI, 2026-10-22): stands. SEL-3: Linz et al. 2017 (mSphere, https://pmc.ncbi.nlm.nih.gov/articles/PMC5489657) describe composition and a core community ("Community composition shifted from year to year ... we detected a core community"); no prediction or target in the source; lake/layer/year as target would replay the sampling design.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

Multiyear 16S rRNA microbiome amplicon (OTU) sequencing of eight bog lakes near Minocqua, Wisconsin, joined from an OTU table and a metadata table. This is microbial-ecology scientific-discovery data: an OTU table is an extremely high-dimensional, sparse compositional matrix with no canonical supervised predictive target, and the multiyear sampling makes it a time series. It does not map to a representative real-world tabular classification/regression task. A human could confirm there is no clear predictive target, but on the available description this should be rejected.

---

Eight bog lakes, multiyear time series of 16s sequences near Minocqua, northern Wisconsin; metadata source: R package "OTUtable", data(metadata); otu table source: https://github.com/McMahonLab/North_Temperate_Lakes-Microbial_Observatory

## Reference

10.1128/mSphere.00169-17
