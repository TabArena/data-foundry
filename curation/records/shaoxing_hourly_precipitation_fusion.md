---
unique_name: shaoxing_hourly_precipitation_fusion
name: Two-stage multi-source hourly precipitation fusion, Shaoxing (rain gauges, radar QPE, IMERG)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Not Available (from Paper))
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.3390/atmos17080762
- https://www.mdpi.com/2073-4433/17/8/762
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Gauge-hour precipitation fusion for Shaoxing: 41,458 hourly samples from 72 rain gauges in the 2025 flood season,
61 features (IMERG, radar QPE with an availability flag, lags and accumulations, neighbourhood, terrain), a LightGBM
wet/dry stage and an XGBoost intensity stage, and a fixed 15-station spatial test set (abstract). The table is not
released. Data Availability Statement (pp. 21-22): "The rain-gauge observations and operational radar QPE data ...
are not publicly available due to data-use restrictions. The derived datasets are available from the corresponding
author upon reasonable request, subject to approval by the original data providers." Unreleased paper data, so the
precedent is `No` with `Not Available (from Paper))`. The task itself (a measured target, grouped by gauge) would be
in scope if the authors deposited the table.

Zero mechanism, from the paper only: dry hours are a threshold. Sec. 2.2: "A threshold of 0.1 mm h-1 was used to
distinguish rainy and non-rainy samples", so trace rain counts as dry. Missing radar values are set to 0 and flagged.

## Reference

Wang H., Zhao L., Ding K., Liu F., Zhang R., Chen L., Qin J., Cao P., Wang S. (2026). A Two-Stage Machine Learning
Framework for High-Resolution Multi-Source Precipitation Fusion in Complex Terrain: A Case Study of Shaoxing, China.
Atmosphere 17(8):762. doi:10.3390/atmos17080762.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 47 (Precipitation fusion - Shaoxing).
