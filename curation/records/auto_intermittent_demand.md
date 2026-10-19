---
unique_name: auto_intermittent_demand
name: Auto intermittent-demand series (Syntetos and Boylan 2005, GluonTS intermittent_auto)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Github
year: '2005'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://github.com/canerturkmen/gluon-ts/tree/intermittent-datasets/datasets
- https://doi.org/10.1371/journal.pone.0259764
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Monthly demand of 3,000 automotive stock-keeping units over 24 months, attributed to Syntetos and Boylan (2005), in
the GluonTS fork of Turkmen et al. (2021). Downloaded on 2026-10-19: 3,000 series x 24 months, 22.0% exact zeros, no
missing values; the only feature is a series id. Turkmen et al., Sec. 5.2: "The Auto data set consists of monthly
demand data for 3000 items, for a period of 24 months"; they keep the 1,227 series classed intermittent or lumpy and
forecast "the last 6 demand periods". Univariate series forecasting, excluded.

Zero mechanism, confirmed from the data: months without demand. With 22% zero cells the full table is only mildly
zero-heavy; the intermittent benchmark is a filtered subset. No data licence stated.

## Reference

Syntetos A.A., Boylan J.E. (2005). The accuracy of intermittent demand estimates. International Journal of
Forecasting 21(2):303-314. Turkmen A.C., Januschowski T., Wang Y., Cemgil A.T. (2021). Forecasting intermittent and
sparse time series: A unified probabilistic framework via deep renewal processes. PLOS ONE 16(11):e0259764.
doi:10.1371/journal.pone.0259764.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 51 (Auto intermittent-demand benchmark).
