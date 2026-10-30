---
unique_name: xente_fraud_detection_challenge
name: xente-fraud-detection-challenge
checked_by:
- Myunghwan
suggestion: 'No'
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/xente-fraud-detection-challenge/data
- https://zindi.africa/competitions/xente-fraud-dection-hackathon
- https://zindi.africa/competitions/indabax-benin-2022/data
- https://zindi.africa/competitions/multimedia-university-of-kenya-hackathon/data
source_row: 927
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: Xente's own e-commerce transactions with a fraud label, a direct fraud-screening task with a dated temporal split.
- Source: Zindi competition "Xente Fraud Detection Challenge" with Xente, Innovation Village and insight2impact, 2019-05-20 to 2019-09-23 (https://zindi.africa/competitions/xente-fraud-detection-challenge, read through Zindi's page API); as published: "a sample of approximately 140,000 transactions that occurred between 15 November 2018 and 15 March 2019"; `training.csv` ("Transactions from 15 November 2018 to 13 February 2019, including whether or not each transaction is fraudulent"), `test.csv` (13 February to 14 March 2019, unlabelled), `Xente_Variable_Definitions.csv`; target `FraudResult` (1 fraud, 0 not); "the data is highly imbalanced". Rows and columns not counted (login).
- Use case: "create a machine learning model to detect fraudulent transactions ... help Xente provide improved and safer service" (Description): Xente scores each transaction as it happens and blocks or reviews it; fit direct if the columns are the transaction fields known at authorisation; regime temporal (the source splits by date; customers recur, so a grouped check is worth one look).
- Siblings and duplicates: the other three links are reruns of the same data: `xente-fraud-dection-hackathon` (Alliance4AI SUP'COM, Nov 2020, API parent `xente-fraud-detection-challenge`), `multimedia-university-of-kenya-hackathon` (Apr 2024, same parent, same Data Description), `indabax-benin-2022` ("La détection des fraudes", Oct 2022, the same "approximately 140,000 transactions ... between 15 November 2018 and 15 March 2019" with the company name removed; also listed in `indabax_hackathons`). Other Xente records are different tasks: `sbtic_xente_credit_scoring_challenge` (loans), `xente_purchase_prediction_challenge` (recommendation). External collections: none found.
- Papers and pages: the competition page and its Evaluation tab; no paper by the publisher; public solutions on GitHub (claims, not read).
- Metric: F1 ("The error metric for this competition is the F1 score", Evaluation tab), on submitted 0/1 labels: a leaderboard metric (MET-4), threshold left to the participant (MET-6; precedent african_credit_scoring_challenge kept `f1`); inputs none.
- Risks for /add-dataset: only `training.csv` is labelled, so a temporal split covers three months with very few frauds per window (TP-5, TP-9); `Amount` and `Value` and the id columns (customer, account, subscription, batch) to check for redundancy and id leakage (LEAK); whether the fraud label is known only after a chargeback, so a gap may be needed (SPLIT).
- Priority: gap 0 (finance, binary, temporal not thin), use case + (Xente named, the decision is the transaction screen), source + (the publisher's dates and variable definitions), shape + (about 140k transactions, mixed types, timestamps), risk - (few positives per temporal window).

Xente fraud detection (Zindi) is a transaction-level financial fraud classification task with a clear binary target (fraudulent vs not) and standard tabular transaction features (amount, channel, product, customer/timestamp). This is a representative real-world tabular classification problem, well known, and likely benefits from a temporal split given timestamps. The main caveats are extreme class imbalance and the need to confirm dataset size and feature usability after cleaning. Provisionally a Yes pending human verification of size, target, and leakage.

CC (2026-10-29, Myunghwan): "This is the suspcious/leaky issue. 80 cases are coverable by simple lookups. In this case, my decision is no." Reject the current Xente candidate because a substantial fraction of the fraud class is concentrated in exact monetary values and is susceptible to lookup/memorization. This final No supersedes earlier screening approval and provisional feature-retention discussion.

**Assessment (AI, 2026-10-29):** The original labelled release has 95,662 transactions and 193 frauds. Amount values 500000, 800000, 3000000 and 5000000 cover 80 frauds (41.45% of all frauds) in 81 rows; the same Value groups cover 79 frauds (40.93%) in 80 rows. Dropping Amount while retaining Value therefore preserves the main signal. The policy fixed before held-out scoring selects Value keys with at least 5 training rows and at least 90% training fraud precision; it identifies 9/14, 5/46 and 17/54 later frauds with zero observed false positives in the oldest/middle/newest chronological windows. The 80/193 full-data count is descriptive, not test recall. These measurements support the curator's case-specific rejection for suspicious shortcut/memorization coverage; they do not demonstrate a particular post-outcome recording mechanism or a whole-task TP-4 triviality proof, so no such marker is added. Low prevalence itself was accepted and label-maturity work was deferred; neither is the reason for rejection. The original category-purity warning alone was not decisive. No Xente definition or container is added; prior raw data, models and independent review are preserved locally.
