---
unique_name: m5_forecasting_accuracy
name: M5 Forecasting - Accuracy (Walmart, Kaggle 2020)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 5
decision_markers:
- Time-series (Forecasting)
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Time-series (Forecasting)`, SEL-10): the fifth Makridakis forecasting
competition, 28-day-ahead point forecasts for each of 42,840 Walmart sales series, scored per series against the
series' own naive forecast, won by recursive and lag-based models.
- Source: the Makridakis Open Forecasting Center (University of Nicosia) with Walmart, on Kaggle, March to June 2020
  (M5 Participants Guide; Makridakis, Spiliotis and Assimakopoulos 2022, IJF 38(4):1346-1364). As published: daily
  unit sales of 30,490 item-store series (3,049 items, 10 stores, 3 states) over 1,941 days, with `calendar.csv`
  (events, SNAP days) and `sell_prices.csv`; the earlier AI triage (2026-10-19) measured 68.0% zero cells, 20.9% of
  all cells leading zeros before an item's first sale.
- Source's words: Kaggle Description: "you will use hierarchical sales data from Walmart ... to forecast daily sales
  for the next 28 days". Participants Guide, Objectives: "The objective of the M5 forecasting competition is to
  advance the theory and practice of forecasting by identifying the method(s) that provide the most accurate point
  forecasts for each of the 42,840 time series of the competition."
- Why TP-10 (SEL-11) does not rescue it: leg 2 fails in the organisers' own account of the winners (results preprint,
  Sec. 4.2): first place, "Two variations were considered for each type of model, the first applying a recursive and
  the second a non-recursive forecasting approach", with features including "unit sales data, both in a recursive
  and a non-recursive format"; third, LSTM layers "used to recursively predict the product-store series"; fifth,
  "recursive LightGBM models"; of the rest of the top 50, "almost all of them adopted similar approaches to the
  winning submission". The winner confirms lags of 28 days and more (forum topic 163684). Leg 1 is thin as well: at
  the product-store level the winner's WRMSSE is 0.884 against 0.926 for Croston's method, 4.5% (Table 5). The
  metric is a series-forecast metric: RMSSE, "a variant of the well-known Mean Absolute Scaled Error", divides each
  series' error by the in-sample error of its one-step naive forecast (Guide, "Point forecasts").
- Use case: Walmart replenishment from item-store forecasts ("setting up appropriate inventory or service levels",
  Kaggle Description), the setting SEL-10 excludes.
- Siblings and duplicates: `walmart_sales_in_stormy_weather` (other Walmart stores, items and years; `Yes`, Andrej 2026-10-30, its scope open in its Review issue 1),
  `rossmann_store_sales` (Yes), `grocery_store_product_forecasting_challenge` (its SEL-10 reject was refuted on
  2026-10-22 because its top solutions were unread; here they are read), `online_retail`; the M5 Uncertainty
  competition (same data, quantiles) has no record.
- Open for the curator (consistency): `rossmann_store_sales` (Yes, Andrej; store-day sales with a 6-week horizon) has
  the same panel shape and has never had TP-10 run. This reject does not reopen it, but the two should be judged
  alike: should Rossmann get the TP-10 test, or what sets it apart from M5 (row-level RMSPE rather than a per-series
  scaled error, store attributes and promotions known ahead)?
- Metric: WRMSSE (Kaggle Evaluation tab; Participants Guide), the leaderboard metric (MET-4); inputs each series'
  training history (the scale) and its dollar sales over the last 28 training days (the weight), over 12 aggregation
  levels; they ship.
- Reject check (AI, 2026-10-27): stands. SEL-10 (Must), TP-10 leg 2 failed. The organisers report that the winning
  approaches forecast recursively from past unit sales and that "almost all" of the top 50 did the same
  (https://statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf, Sec. 4.2).

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 5 (the AI screening had `No`; zero-inflated screening review page).
"This is a great dataset, would just need more evidence to decide how to treat the time series aspect"

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 49 (M5 Forecasting - Accuracy (Walmart)).
