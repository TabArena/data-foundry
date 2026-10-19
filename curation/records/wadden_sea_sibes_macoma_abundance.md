---
unique_name: wadden_sea_sibes_macoma_abundance
name: Wadden Sea Macoma abundance (Lyashevska et al. 2016) / SIBES synoptic intertidal benthic survey (NIOZ, 2008-2022)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Website
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.25850/nioz/7b.b.ug
- https://doi.org/10.1038/s41597-025-04540-9
- https://doi.org/10.1002/ece3.1880
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

The workbook row is Lyashevska et al. (2016), a spatial zero-inflated Poisson model of the bivalve Macoma balthica in
the Dutch Wadden Sea. That paper released no table (its only supplement is a key-terms table), and its "3,451" is the
number of 2010 grid stations, not of counts. Its data come from SIBES, NIOZ's synoptic intertidal benthic survey,
which is public as a whole, so this record points there. Downloaded the SIBES release (18 MB) on 2026-10-19: 59,463
core samples from 2008-2022 at 5,105 stations (most sampled 13-15 years) and 171 taxa, with coordinates, grain size,
mud content, tidal basin, date and platform. The paper's use is predictive: "The model is used for prediction and
mapping the abundance of a benthic invertebrate" (Introduction), judged by leave-one-out cross-validation.

Zero mechanism, confirmed from the data: no Macoma in the core. Macoma (`sibes_id` 59) appears only as presence rows
in `biota.csv`, so the zeros come from filling against `samples.csv`: 56.2% overall, 42-72% by year. The paper's
Bernoulli/Poisson split is a model assumption. A quick LightGBM on log1p density: R^2 0.36 grouped by station
(presence AUC 0.81), 0.26 from sediment and date alone, 0.28 on 2021-22 as a temporal test. To check: whether a thin
feature set (coordinates, sediment, date) is wanted; the taxon (Macoma follows the paper); 769 samples without any
biota row (empty cores or missing records); sediment is missing in 3,687 samples, and the paper's elevation covariate
is not in the release. Licence: CC BY-SA 4.0; the latest three years are embargoed.

## Reference

Lyashevska O., Brus D.J., van der Meer J. (2016). Mapping species abundance by a spatial zero-inflated Poisson model:
a case study in the Wadden Sea, the Netherlands. Ecology and Evolution 6:532-543. doi:10.1002/ece3.1880. SIBES:
Bijleveld A.I. et al. (2025), Scientific Data, doi:10.1038/s41597-025-04540-9; data doi:10.25850/nioz/7b.b.ug.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 20 (Wadden Sea Macoma abundance).
