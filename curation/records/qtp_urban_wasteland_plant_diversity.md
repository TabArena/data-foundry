---
unique_name: qtp_urban_wasteland_plant_diversity
name: Spontaneous plant diversity in urban wastelands, 17 cities of the Qinghai-Tibet Plateau
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: a one-season survey of 585 plots in 38 urban
wastelands of 17 cities with climate, urbanization and habitat covariates; the source's aim is a driver analysis, and
since it is a broad survey and not an experiment, the family's open species-abundance question decides it rather than
a fast reject; every predictor is constant within a wasteland.
- Source: He, Gao, Yao et al. 2026 (Ecology and Evolution 16:e73521, read via PMC13128321); Dryad
  doi:10.5061/dryad.r7sqv9sst (2026-04-22, CC0), one zip. As published (earlier AI triage, 2026-10-19, measured on the
  identical supplement): Total, Native, Non-native and Invasive tables of 585 plots each with 24-27 predictors and 38
  wastelands, against the paper's "590 1 × 1 m herbaceous plots" and "41 wastelands" (Sec. 2.2.1).
- Use case: the aim is understanding, "addressing our core question of how climate, urbanization, and habitat
  structure shape wasteland communities" (Sec. 2.3); "the study aims to advance a more comprehensive understanding of
  urban biodiversity in high-altitude environments" (Introduction); the advice in Sec. 4.5 is general. For example a
  city planner estimating the non-native richness of a wasteland before choosing invasion control; no actor named, fit
  approximate at best. Regime grouped by wasteland (SPLIT-3).
- Siblings and duplicates: none among the records (searched for wasteland, Qinghai). External collections: none found.
- Papers and pages: the paper (Introduction, Sec. 2.2-2.3, 4.5); preprint doi:10.22541/au.176565615.53590545/v1.
- Metric: none for prediction (GLMMs with nested random intercepts, the fixed effects ranked by their share of the
  marginal R2, Sec. 2.3), so the fallback `rmse`.
- Risks for /add-dataset: 38 effective units, since every predictor is constant within a wasteland (earlier AI triage
  measured LightGBM grouped by wasteland at R2 0.195 and ridge at -0.01 for non-native richness); the Shannon, Simpson
  and Pielou indices are 0 by definition for one-species plots (24-26% of rows), so only the richness counts are
  candidate targets; plots were placed "in representative plant communities with vegetation cover ≥ 30%" (Sec.
  2.2.1). Open question: species-abundance mapping from habitat covariates; `No Good Target / Scientific Discovery`
  stays as the marker of that concern.
- Priority: gap 0, use case 0, source + (paper and CC0 deposit, measured), shape 0 (585 plots, 38 units), risk - (38
  units, index targets zero by construction).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page).
No reason was given on the page; the record's markers (`No Good Target / Scientific Discovery`) stand as the reason.

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 43 (Spontaneous plant diversity in urban
wastelands).
