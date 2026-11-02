---
unique_name: jane_street_real_time_market_data_forecasting
name: Jane Street
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- tabular-dl-more-data
original_source: Kaggle
year: '2024'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting
- https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/data
- https://arxiv.org/abs/2610.26794
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a large market panel from Jane Street's production systems, scored by the host's weighted R²; anonymized throughout, and whether it is forecasting (SEL-10) is for TP-10 to settle, as it was for `g_research_crypto_forecasting`.
- Source: Jane Street, Kaggle Featured competition "Jane Street Real-Time Market Data Forecasting" (opened 2024-10-14, final submissions 2025-01-13, then a forecasting phase on live market data to 2025-07-14; 3,757 teams). Data page: "The competition dataset comprises a set of timeseries with 79 features and 9 responders, anonymized but representing real market data. The goal of the competition is to forecast one of these responders, i.e., `responder_6`, for up to six months in the future." As published: train.parquet in ten partitions (12.3 GB; the row count was not read), one row per `symbol_id` x `date_id` x `time_id` (ordinal integers, no calendar dates; "the actual time intervals between `time_id` values may vary"); `weight`; `feature_00` to `feature_78` ("Anonymized market data"); `responder_0` to `responder_8` ("Anonymized responders clipped between -5 and 5"); lags.parquet holds all responders "lagged by one `date_id`", served at each day's first time step; features.csv and responders.csv hold anonymous tags only (responders.csv previewed); the training-phase test set "has about 4.5 million rows".
- Use case: Jane Street's automated trading ("real-world data derived from some of our production systems", "markets where we run automated trading strategies"): at each time step, predict a symbol's response and trade on it; fit approximate (the responder, its horizon and the instruments are hidden); regime temporal: the host scores later dates through an API that "ensures that models do not peek forward in time".
- Siblings and duplicates: no other record of this competition; Jane Street's earlier Kaggle competition (Jane Street Market Prediction, 2020-21) has no record. Precedents: `g_research_crypto_forecasting` (a "forecasting competition" kept after TP-10 was amended, Lennart 2026-10-22), `numerai_v5_2` (an anonymized weekly stock panel, `Yes`); `stock` stays retired as forecasting. External collections: tabular-dl-more-data (Rubachev, Lazarev, Babenko 2026, arXiv 2610.26794, "Jane Street": 10.00M train / 93K validation / 93K test, 94 features with lag features built "following the competition protocol and public solutions", the last two periods of 100 dates as validation and test, RMSE).
- Better data: a candidate of the benchmark tabular-dl-more-data; no further search this round.
- Papers and pages: the competition's Overview, Evaluation, Data, Timeline and Rules pages (read through the Kaggle API, 2026-10-31); the 8th-place private-LB writeup (Kaggle discussion 556542: a GRU over each day's sequence, rolling and market-average features, `responder_7` and `responder_8` as auxiliary targets, online learning on the served responders; it relays a forum finding that `responder_6` is a 20-day rolling average); Rubachev et al. 2026.
- Metric: the "sample weighted zero-mean R-squared score" of `responder_6`, R² = 1 − Σ w (y − ŷ)² / Σ w y² (the Evaluation page); the competition's metric, deliberate (MET-4); inputs: `weight`, which ships in train.parquet and becomes a scoring column (MET-2).
- Risks for /add-dataset: scope (SEL-10, SEL-11, TP-10): the host calls it "a forecasting competition" on "a set of timeseries" and serves the previous day's responders as inputs, and the writeup read relies on a sequence model with online learning; leg 2 (no lag of the target beyond its last known observation) and leg 1 (beat each symbol's naive forecast under the weighted R²) both need the check; the other eight responders are same-window outcomes, never features (LEAK-10); whether `weight` is also a feature is a choice to make; no calendar dates, and the number of `time_id`s per day changes over the history (the writeup starts at `date_id` 700); `Anonymized` set from the source's words (features, responders and encrypted `symbol_id`; LEAK-32). Data use: "You may access and use the Competition Data only for participating in the Competition and on Kaggle.com forums" (Rules 7.A; no criterion, EV-4).
- Priority: gap 0 (finance, regression and temporal not thin), use case 0 (the actor is named, the target and horizon are hidden: fit approximate), source + (the host's data page documents every column), shape + (12.3 GB of rows, 79 features, a time structure), risk - (the forecasting scope is open).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark tabular-dl-more-data (https://arxiv.org/abs/2610.26794).
- as published: 10.00M train / 93K val / 93K test, 94 features (anonymized feature_00..78 without feature_61, symbol_id and time_id as categoricals, periodic encodings and lag features built by the authors); ...; target: responder_6 (anonymized; the other eight responders are dropped as same-window leaks).
- Why: Predict an anonymized market response for a symbol at a time step from anonymized market features (Jane Street Kaggle competition, 2024)
- Notes: Fully anonymized financial data with no calendar dates; a return forecasting task with lagged responders as features, so a SEL-10 Time-series (Forecasting) case unless it passes TP-10. Kaggle competition data: check the competition's data-use rules. Raw train.parquet comes as hive partitions.
