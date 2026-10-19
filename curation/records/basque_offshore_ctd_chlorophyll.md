---
unique_name: basque_offshore_ctd_chlorophyll
name: Hydrographic benchmark (marine-ml-benchmark "hydrographic") / CTD profiles at Mendexa offshore aquaculture (AZTI)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Github
year: '2025'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/zhm12305/marine-ml-benchmark
- https://doi.org/10.1371/journal.pone.0351325
- https://doi.org/10.17632/vyz9zvddz4.2
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

The "hydrographic" table of the same benchmark as `basque_offshore_bivalve_biotoxins`, from the same AZTI upstream.
The raw file is 8,195 rows of 1-dbar CTD depth bins from 2 stations on 146 dates (May 2014 to December 2023);
reproducing the repository's pipeline (quality control plus an IQR filter) gives exactly the paper's 4,653 rows from
132 casts with 11 predictors (latitude, longitude, time of day, pressure, temperature, salinity, sigma-theta, light
transmission, PAR, dissolved oxygen, oxygen saturation). The task is predicting fluorometer chlorophyll from the
other sensor channels of the same cast, which has no use case; rows within a cast are dependent, the IQR filter cuts
the bloom values, and the "nutrient concentrations" the paper mentions are not in the file. -999 missing codes occur
in PAR (297), salinity (95) and temperature (47).

Zero mechanism, confirmed from the data: none, chlorophyll has no exact zeros (minimum 0.03). Workbook pushback: "not
clearly established" is generous; the target has no zero regime at all.

## Reference

Zhou X., Zhang H., Du T., Yuan Q., Wang H. (2026). Cross-dataset benchmarking of machine learning models for marine
and atmospheric environmental prediction. PLOS ONE. doi:10.1371/journal.pone.0351325. Upstream: Solaun O. et al.
(2025). Data in Brief 61:111736; data doi:10.17632/vyz9zvddz4.2.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 27 (Hydrographic benchmark).
