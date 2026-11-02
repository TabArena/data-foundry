---
unique_name: google_analytics_customer_revenue_prediction
name: Google Analytics Customer Revenue Prediction (Kaggle 2018, Google Merchandise Store / GStore)
checked_by:
- Andrej
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Kaggle
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/ga-customer-revenue-prediction
- https://support.google.com/analytics/answer/7586738
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: a future-revenue task per customer with the competition's
metric, but it must be rebuilt from 25 GB of nested session logs and leaves about 130 buyers per window (earlier AI
triage, 2026-10-20, measured on v1), so the amount part may not be learnable.
- Source: Kaggle competition by RStudio and Google Cloud, 2018-09-13 to 2019-02-21 (Kaggle API: "Predict how much GStore
  customers will spend"); files train_v2.csv (25.4 GB) and test_v2.csv (7.6 GB), plus the withdrawn v1 train.csv and
  test.csv (Kaggle API file list, 2026-10-27). The sessions are Google Analytics 360 data of the Google Merchandise
  Store; v1's train period is that of Google's public BigQuery GA sample (not compared row by row).
- Use case: for example, the store's marketing team sets its spend per customer from the predicted revenue of the coming
  months (the competition's framing; the overview does not render here); fit approximate (windows rebuilt, the scored
  target window of Dec 2018 to Jan 2019 never released). Regime temporal: feature window, 46-day gap, 62-day target
  window, as the winner built them (discussion 82614, earlier AI triage).
- Siblings and duplicates: `online_shoppers_purchasing_intention_dataset` (Yes) is another store's sessions (UCI), other
  data. External collections: none found.
- Papers and pages: discussions 68353 (v1 relaunched: test revenue readable in Google's demo account), 81531 and 82614
  (the all-zero submission scored 0.88843 against the winner's 0.88140), 81542 (earlier AI triage).
- Metric: RMSE (Kaggle API, "Root Mean Squared Error") on the natural log of each user's summed revenue plus one
  (third-party write-ups; the Evaluation tab does not render here), so `rmsle` on the summed revenue with
  `target_transform="log1p"` (MET-3, MET-4); inputs: the per-user sum over the target window.
- Risks for /add-dataset: heavy wrangling (JSON columns, user windows; `Needs extensive data wrangling` kept); a visit's
  own pageviews give away its purchase (AUC 0.98 on v1, earlier AI), so features come from the feature window only
  (LEAK-10); 131 and 138 buyers in two windows (TP-5); whether the GA sample is random (12th place write-up). No open
  family question applies (a visit without purchase has no revenue field, an observed zero).
- Priority: gap 0 (business & marketing), use case 0 (fit approximate), source + (Google's GA sample documentation),
  shape + (about 300,000 users per window, temporal), risk - (a heavy rebuild, few buyers).

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated
screening review page).

Kaggle competition by RStudio and Google Cloud (2018) on obfuscated Google Analytics 360 visits to the Google
Merchandise Store; the v1 train window (Aug 2016 to Aug 2017) is the period of Google's public BigQuery GA sample (not
compared row by row). v1 was relaunched because its test-period revenue could be read in Google's demo GA account
(discussion 68353). v2 (data page): train_v2 (Aug 2016 to Apr 2018, 25 GB) and test_v2 (May to Oct 2018), target
ln(1 + summed `totals.transactionRevenue`) per user over Dec 2018 to Jan 2019, which was never released. Zero
mechanism, confirmed on v1: a visit without purchase has no revenue field (no explicit zeros, no negatives). v1
train.csv: 903,653 visits, 714,167 users, 98.7% of visits without revenue. Rebuilt as the v2 task inside v1 (feature
window, 46-day gap, 62-day target window), 131 of 295,432 users bought in one window and 138 of 368,904 in the next
(99.96% zeros).

Probe (untuned LightGBM, 18 user features, earlier window to the later one): ROC AUC 0.81 for a purchase, R^2 -0.03 on
log1p revenue among the 138 buyers. On the private leaderboard the all-zero submission scored 0.88843 against the
winner's 0.88140 (discussions 81531, 82614). Split: temporal user windows as the winner built them (168-day features,
46-day gap, 62-day target; discussion 82614) from train_v2 plus test_v2, which carries revenue too. Features must come
from the feature window only: a visit's own pageviews give away a purchase in that visit (AUC 0.98 alone on v1).
Terms: Kaggle rules, non-commercial use including research and education. To check: whether 100-400 buyers per window
carry a regression task or only a classification one, and whether the GA sample was drawn non-randomly (12th place
write-up, discussion 81542).

## Reference

Google Analytics Customer Revenue Prediction. Kaggle competition hosted by RStudio and Google Cloud, 2018.
https://www.kaggle.com/competitions/ga-customer-revenue-prediction. Underlying data: Google Analytics 360 sample of the
Google Merchandise Store (BigQuery public dataset), https://support.google.com/analytics/answer/7586738.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
