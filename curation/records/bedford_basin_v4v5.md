---
unique_name: bedford_basin_v4v5
name: bedford_basin_V4V5
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- 'DF: Suspended'
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- '?'
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
problem_type: Other
original_data_state: Other
source_row: 793
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): the Bedford Basin V4-V5 16S ASV table is published for a descriptive study of phytoplankton community dynamics, not for a prediction; no target is named.
- Source: Robicheau, Tolman, Bertrand and LaRoche, "Highly-resolved interannual phytoplankton community dynamics of the coastal Northwest Atlantic", ISME Communications 2, 38 (2022), doi 10.1038/s43705-022-00119-2; weekly samples at 1, 5, 10 and 60 m of the Bedford Basin time-series station, 16S V4-V5 2014-2017, flow cytometry 2014-2018; ASV tables in the supplementary data; metadata from the Bedford Basin Monitoring Program.
- Use case: none; the paper characterises seasonal and interannual shifts, indicator taxa and networks (indicator species analysis, NMDS, envfit, CoNet), and fits no model to predict anything; any target (depth, season, temperature from the ASVs) would be our own (USE-1, USE-2).
- Siblings and duplicates: `bedford_basin_v6v8` is the V6-V8 amplicon of the same samples (a cut of one dataset, PROV-6); the other microbiome records of the same import (`bog_lakes`, `boso_fish`, `tara_oceans`, `eu_lakes_*`, `subseafloor_*`, `nz_springs`, `ports`, `australia`, `atl_ocean_transect`, `wastewater_treatment`) are all AI-screened, no human verdict. The record's `DF: Suspended` status is kept.
- Metric: none (no prediction in the paper).
- Reject check (AI, 2026-10-22): stands. SEL-3 (Must): the source is a descriptive study ("high-frequency DNA sampling allows for the detection of shifting baselines in phytoplankton communities", Robicheau et al. 2022, https://academic.oup.com/ismecommun/article/7461061); indicator species, NMDS, networks, no model and no target; any target (depth, season) would be ours. Same call as all 13 sibling microbiome records in this rescreen.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

Bedford Basin Monitoring Program microbiome data (V4V5 amplicon region) with an OTU table from a paper's supplementary information; the record is already marked 'DF: Suspended' and tagged '?'. This is microbial-ecology OTU data for scientific monitoring/discovery, lacking a well-defined real-world predictive target and not representative of tabular ML (sparse high-dimensional OTU matrix). The suspended status and discovery framing are decisive. Excluded; a human can confirm the suspension rationale.

---

Multiyear monitoring in the Bedford Basin Monitoring Program; metadata source: https://www.bio.gc.ca/science/monitoring-monitorage/bbmp-pobb/bbmp-pobb-en.php (TODO); otu table source: SI Table 2

## Reference

10.1038/s43705-022-00119-2
