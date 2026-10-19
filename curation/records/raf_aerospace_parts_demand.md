---
unique_name: raf_aerospace_parts_demand
name: RAF aerospace spare-parts demand (Eaves and Kingsman 2004, GluonTS intermittent_raf)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Github
year: '2004'
domain: industry & manufacturing
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

Monthly demand of 5,000 Royal Air Force spare parts over 84 months, attributed to Eaves and Kingsman (2004), in the
same GluonTS fork as `auto_intermittent_demand`. Downloaded on 2026-10-19: 5,000 series x 84 months, 89.8% exact
zeros, no missing values, a series id as the only feature. Turkmen et al. (2021, Sec. 5.2) hold out the last 6
periods. Univariate series forecasting, excluded.

Zero mechanism, confirmed from the data: months without demand for slow-moving spares. The alternative copy the
workbook names (github.com/danieldehaan96/spdf) was not compared. No data licence stated.

## Reference

Eaves A.H.C., Kingsman B.G. (2004). Forecasting for the ordering and stock-holding of spare parts. Journal of the
Operational Research Society 55(4):431-437. Used in Turkmen A.C. et al. (2021), PLOS ONE 16(11):e0259764.
doi:10.1371/journal.pone.0259764.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 52 (RAF aerospace-parts demand).
