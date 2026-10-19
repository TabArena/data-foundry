---
unique_name: qtp_urban_wasteland_plant_diversity
name: Spontaneous plant diversity in urban wastelands, 17 cities of the Qinghai-Tibet Plateau
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.r7sqv9sst
- https://doi.org/10.1002/ece3.73521
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Plot-level richness and diversity of spontaneous plants in urban wastelands (He, Gao, Yao et al. 2026). The workbook's
title and its "Qinghai-Tibet Plateau vegetation" description are the same study. Downloaded the paper's supplement
("Code and data", identical files to Dryad) on 2026-10-19: Total, Native, Non-native and Invasive tables of 585 plots
each with 24-27 predictors, from 38 wastelands in 17 cities, one season (July-August 2024), no missing values. Every
predictor is constant within a wasteland, so there are 38 effective units. The aim is "identify the key drivers"
(Introduction) with GLMMs "with nested random intercepts (CityID/WastelandID)".

Zero mechanism, confirmed from the data: no non-native or invasive species in a 1 m2 plot (56.4% and 62.1% zeros of
the richness). For the Shannon, Simpson and Pielou indices (82.6-86.2% zeros), a further 24-26% of rows are
one-species plots whose index is 0 by definition, an artefact. A wasteland-level model can at best explain R^2 0.38
of non-native richness in sample; LightGBM grouped by wasteland reaches 0.195 and ridge -0.01. The files hold 585
plots and 38 wastelands against the paper's 590 and 41. Licence: CC0.

## Reference

He L., Gao Z., Yao Y., et al. (2026). Patterns and drivers of spontaneous plant diversity in urban wastelands across
17 cities on the Qinghai-Tibet Plateau. Ecology and Evolution 16:e73521. doi:10.1002/ece3.73521. Data:
doi:10.5061/dryad.r7sqv9sst.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 43 (Spontaneous plant diversity in urban
wastelands).
