---
unique_name: ga_merchandise_store_sessions
name: Google Analytics sample dataset for BigQuery (Google Merchandise Store, obfuscated GA360 sessions)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Company
domain: business & marketing
source_links:
- https://support.google.com/analytics/answer/7586738
- https://www.kaggle.com/competitions/ga-customer-revenue-prediction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: Google's obfuscated GA360 export of a real online store, the data of a Kaggle Featured competition (2018-2019, 3,611 teams) scored on per-customer revenue by RMSE; real and large, but the first round's test revenue could be read from Google's public demo account, ids are obfuscated, and the session-level purchase task the scouts propose is ours to define.
- Source: Google, "Google Analytics sample dataset for BigQuery" (bigquery-public-data.google_analytics_sample.ga_sessions_*): "obfuscated Google Analytics 360 data from the Google Merchandise Store", with example queries "for the period of 1-Aug-2016 to 1-Aug-2017"; "Data for some fields have been obfuscated such as fullVisitorId", others "removed such as clientId, adWordsClickInfo and geoNetwork"; the stated purpose is "exploring the benefits of exporting Google Analytics 360 data into BigQuery" (https://support.google.com/analytics/answer/7586738). Reused in Kaggle's "Google Analytics Customer Revenue Prediction" ("Predict how much GStore customers will spend"; opened 2018-09-13, deadline 2019-02-21, per the Kaggle API). As published there: train.csv (1.5 GB) and test.csv (1.3 GB), then, after the relaunch, train_v2.csv (25.4 GB, with hit-level JSON) and test_v2.csv (7.6 GB); one row per session with JSON columns (device, geoNetwork, totals, trafficSource, hits); row counts not read (about 0.9 M sessions in train.csv, from memory).
- Use case: the competition's: predict each customer's revenue in a later window, for the store's marketing spend (the Overview page needs JavaScript and was not read; the API description says only "Predict how much GStore customers will spend"); the scouts' alternative is a purchase within a session predicted during it (the `online_shoppers_purchasing_intention_dataset` setting), which needs a prediction point cut from the hits. Fit approximate; regime temporal (v2 scored revenue in a window after the last session, from memory).
- Siblings and duplicates: `online_shoppers_purchasing_intention_dataset` (`Yes`, sessions of another store, Sakar et al. 2019: another source with the same unit and target, PROV-4); `customer_propensity_to_purchase_dataset` (`No`, generated) and `customer_acquisition_data` (`No`, untraceable); no other GStore record (searched gstore, merchandise store, the slugs and the help-page id). External collections: none known.
- Better data: no new search; found as better data for `online_shoppers_purchasing_intention_dataset`, `customer_propensity_to_purchase_dataset` and `customer_acquisition_data`.
- Papers and pages: Google's help page (read); the Kaggle competition (Overview, Evaluation and top solutions not read).
- Metric: the competition's RMSE (Kaggle API evaluationMetric "Root Mean Squared Error"; on the natural log of each user's summed revenue plus one, from memory of the Evaluation tab, which could not be read): a leaderboard metric (MET-4). Inputs: the user id (fullVisitorId) to sum per user, ships. A session purchase task would have no source metric (fallback `roc_auc`).
- Risks for /add-dataset: the first round's test revenue was public through the GA demo account, the reason for the v2 relaunch (check that no shipped field can be looked up); session totals (pageviews, hits, timeOnSite, transactions, revenue) cover the whole session, after any purchase (LEAK for a session task: cut from the hits); obfuscated ids and removed fields; about 99% of users have zero revenue; the v2 scoring window is not in the public files (from memory), so a revenue window is ours to construct from the sessions (SPLIT-9); 25 GB of nested JSON to flatten.
- Priority: gap 0 (business, regression and temporal are not thin), use case 0 (the publisher states a demo purpose; the competition's Overview was not read), source + (Google's documented export and a Featured competition), shape + (about a million sessions or more, mixed types, over a year), risk - (a leak history, totals after the purchase, a target window to construct).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `customer_acquisition_data`, `customer_propensity_to_purchase_dataset`, `online_shoppers_purchasing_intention_dataset`.
- as published: one row per session of a real e-commerce store with traffic source, device, geography, totals (pageviews, hits, time on site, bounces, transactions, revenue) and nested hit-level page data; Kaggle ...; target: the session ends in a transaction (totals.transactions > 0), or its revenue; access: registration (Google Cloud account for BigQuery, or Kaggle account and competition rules).
- Why: Same unit (a session), same target (purchase in the session) and the same kinds of features as online_shoppers (pages and time per page type, bounce and exit behaviour, traffic source, device, region, month), from a real store | customer_propensity_to_purchase_dataset is a fictional site's day of visits with on-site ...
- Adds: About 70x the sessions over a full year and the hit-level timeline, so features can be cut at a prediction point inside the session (the record's open concern about features computed after the purchase); no PageValues column, whose early-period leak cost the old data 5,455 rows. Caveats: fullVisitorId obfuscated and ...
