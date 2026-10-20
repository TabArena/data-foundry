---
unique_name: google_analytics_customer_revenue_prediction
name: Google Analytics Customer Revenue Prediction (Kaggle 2018, Google Merchandise Store / GStore)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
