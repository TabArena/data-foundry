---
unique_name: carbonfluxbench_flux_tower_upscaling
name: CarbonFluxBench / CarbonBench (daily eddy-covariance fluxes of 479 towers, spatial upscaling benchmark)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Other
year: '2026'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://huggingface.co/datasets/alexroz/CarbonFluxBench
- https://github.com/alexxxroz/CarbonFluxBench
- https://arxiv.org/abs/2603.09868
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Daily eddy-covariance fluxes (GPP, RECO, NEE) of 479 towers from AmeriFlux, FLUXNET2015, ICOS and JapanFlux,
1991-2024, with MODIS reflectance and ERA5-Land drivers (University of Minnesota). The paper builds it for "zero-shot
spatial transfer in carbon flux upscaling" (abstract) with "a hold-out strategy that partitions sites" (Sec. 2.1.1),
i.e. a regression grouped by site, and finds LightGBM "competitive with temporal models on GPP" (Sec. 6.1).
Downloaded `target_fluxes_v2.parquet` on 2026-10-19: 1,262,112 site-days, -9999 for missing (4.4% for GPP and RECO,
1.4% for NEE). The feature files (MODIS 474 MB, ERA5 5.0 GB) were not downloaded.

Not a zero-regime dataset: exact zeros are 0.000% for GPP and NEE and 0.53% for RECO, and NEE is negative on 49% of
the days. The paper's "zero at night" is about the sub-daily cycle. It stays a candidate on its merits, not as part of
this family. To check: whether MODIS reflectance at the tower pixel falls under the remote-sensing exclusion (ERA5
and site metadata alone still make a task); the target (NEE is measured, GPP and RECO come from partitioning); testing
on QC = 1 rows as the paper does (Sec. 5.1); site and row counts, which differ between the card (573 sites,
1,405,813 rows), the README (474, 1.1M) and the file. Licence: MIT on the repository; the flux data keep their
networks' policies (AmeriFlux requires site citations).

## Reference

Rozanov A., Renganathan A., Zhang Y., Kumar V. (2026). CarbonBench (released as CarbonFluxBench). arXiv:2603.09868.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 25 (CarbonFluxBench).
