---
unique_name: boso_fish
name: boso_fish
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
original_data_state: Database (or multiple to-be-joined tables)
source_row: 795
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): the Boso Peninsula fish eDNA metabarcoding series is published to infer fish-fish interaction strengths and their temperature sensitivity, not for a prediction; no target is named.
- Source: Ushio, Sado, Fukuchi, Sasano, Masuda, Osada and Miya, "Temperature sensitivity of the interspecific interaction strength of coastal marine fish communities", eLife 12, RP85795 (2023), doi 10.7554/eLife.85795; 550 seawater samples, 11 sites, twice a month, 2017-08 to 2019-08, 1,130 MOTUs (top 50 species analysed), covariates water temperature, salinity, wave height, tide; data on Zenodo 7865959, reads in DDBJ DRA014111.
- Use case: none; the study uses information-theoretic causality and the MDR S-map on the species series; a target (a species' abundance next sample) would be forecasting a series (SEL-10) and anything else our own (USE-1, USE-2).
- Siblings and duplicates: the other microbiome records of the same import (all AI-screened). `DF: Suspended` kept.
- Metric: none.
- Reject check (AI, 2026-10-22): stands. SEL-3: Ushio et al. 2023 (https://elifesciences.org/articles/85795) infer interaction strengths ("We detected fish-fish interactions as information flow between eDNA time series"); the quantity explained is an estimated interaction strength, forecasting is named only as future work; a next-sample abundance target would also be SEL-10.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

Fish environmental-DNA (eDNA) metabarcoding from seawater sampled twice monthly at 11 coastal sites over two years on the Boso Peninsula, Japan. Like other amplicon/OTU datasets this is a high-dimensional sparse compositional metabarcoding table from an ecology study with no canonical supervised target, and it is already flagged 'DF: Suspended'. It is a temporal scientific-discovery dataset, not a representative tabular predictive task. Reject; a human need only confirm the absence of a usable supervised target.

---

Fish eDNA metabarcoding on seawater samples collected twice a month from 11 coastal sites for 2 years in the Boso Peninsula, Japan; metadata source: https://zenodo.org/records/7865959; otu table source: https://zenodo.org/records/7865959

## Reference

10.7554/eLife.85795.3
