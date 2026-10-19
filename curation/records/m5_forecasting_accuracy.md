---
unique_name: m5_forecasting_accuracy
name: M5 Forecasting - Accuracy (Walmart, Kaggle 2020)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Kaggle
year: '2020'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/m5-forecasting-accuracy
- https://www.unic.ac.cy/iff/research/forecasting/m5-competition/
- https://doi.org/10.1016/j.ijforecast.2021.11.013
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

The M5 competition (University of Nicosia with Walmart): daily unit sales of 30,490 item-store series (3,049 items,
10 stores, 3 states) over 1,941 days, with calendar and price files. The organisers ask for "28 days ahead point
forecasts" across the hierarchy, which is series forecasting over a horizon and excluded. Measured on
`sales_train_evaluation.csv` (2026-10-19): 68.0% of the cells are exact zeros; 20.9% of all cells are leading zeros
before an item's first sale, and 59.5% of the cells after the first sale are zero.

Zero mechanism: an item not yet on sale (the leading zeros, confirmed from the data), no demand, or a stockout the data
cannot show (there is no inventory column). Tension with `rossmann_store_sales` (shipped temporal Yes, store-day sales
with a given horizon): M5 has the same shape at item level, but its source task is the 28-day forecast of 30,490
series, so it stays No. Licence: the competition rules (not read).

## Reference

Makridakis S., Spiliotis E., Assimakopoulos V. (2022). M5 accuracy competition: Results, findings, and conclusions.
International Journal of Forecasting 38(4):1346-1364. doi:10.1016/j.ijforecast.2021.11.013.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 49 (M5 Forecasting - Accuracy (Walmart)).
