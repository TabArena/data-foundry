---
unique_name: absa_customer_income_prediction_challenge
name: absa-customer-income-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- New IID
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: finance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/absa-customer-income-prediction-challenge/data
- https://zindi.africa/competitions/absa-customer-income-prediction-challenge
- '# discussions: winners, the income-bracket baseline (16527); declared income vs band (15094, 15312)'
- https://zindi.africa/competitions/absa-customer-income-prediction-challenge/discussions/16527
- '# a participant''s solution (Pieterkii), shows the file schema'
- https://github.com/Pieter-Cawood/Bank-Customer-Income-Prediction/blob/main/code.ipynb
- '# public copy of customer.csv, income_group.csv, employment_status.csv only'
- https://github.com/Phosamalebo/Absa-Customer-Income-Prediction
source_row: 896
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: a bank predicting a retail customer's declared net income from 14 months of transactions; a real per-customer regression, held back by the income-band leak, a heavy join and access.
- Source: Zindi, "Absa Customer Income Prediction Challenge", 29 Nov 2022 to 26 Feb 2023, Absa (https://zindi.africa/competitions/absa-customer-income-prediction-challenge, read through Zindi's page API); as published: "5144 customers and 46926 unique accounts", transactions "from the start of July 2021 to the end of August 2022" (transactions.csv, 448 MB), Train.csv with "3600 customers along with their declared net income", Test.csv with 1,544 unlabelled customers, customer.csv (demographics), income_group.csv, employment_status.csv.
- Use case: "This solution will enable Absa to anticipate their customers' needs, and allow them to offer optimal solutions to their customers" (Description): the bank estimates income to tailor offers; fit direct for an income estimate at the declaration date; regime IID over customers (one declaration each).
- Siblings and duplicates: `absa_corporate_client_activity_forecasting_challenge` is another dataset (corporate client events). Other income records (`income_prediction_challenge_for_azubian`, `predictive_insights_youth_income_prediction_challenge`, `adult`) are other populations. External collections: none found.
- Papers and pages: no paper; discussions 14806, 15094, 15312, 16527 and the solution notebook in `source_links` (the 2026-10-14 assessment below has the details).
- Metric: RMSE on the declared income ("The error metric for this competition is the Root Mean Squared Error", Evaluation tab); MET-4; inputs none.
- Risks for /add-dataset: `INCOME_GROUP_CODE` is a band of the same income: drop it (LEAK); `DATE_LAST_UPDATED` falls after `RECORD_DATE`; aggregate transactions up to each `RECORD_DATE` (LEAK, temporal); the target is self-declared (noise); only the 3,600 train customers are labelled; access: login, a South-Africa-only competition (no criterion, EV-4).
- Priority: gap 0 (finance, regression, IID are not thin), use case + (Absa names its use), source 0 (a competition page), shape + (3,600 customers, transactions plus demographics), risk - (the band leak and a 448 MB join).

Predict a bank customer's income from their transaction history, tagged 'New IID' by curators. This is a genuine real-world tabular regression task in finance with a clear, meaningful target. The main caveat is that transaction-level data must be aggregated to one row per customer, so it requires non-trivial feature engineering and the final row count after wrangling is unknown. A human must verify the post-aggregation table size, that the target is true income (not leakage from balance), and the absence of ethical issues around financial profiling.

**Assessment (AI, 2026-10-14):** recommend keeping `TBD -> Yes` with `Needs extensive data wrangling`, on two conditions: `INCOME_GROUP_CODE` is dropped, and someone can download the data from Zindi. The human has the call.

* **Data** (Zindi data page): `Train.csv` holds 3,600 customers with `RECORD_DATE` (the month of the declaration, 2022) and `DECLARED_NET_INCOME` (rand, a comma-formatted string). The 1,544 customers of `Test.csv` have no labels. The features come from `customer.csv` (sex, age, occupational status, number of accounts, income group) and from `transactions.csv` (448 MB, Jul 2021 to Aug 2022: amount, balance, description, channel and product per transaction), aggregated to one row per customer. The split is IID over customers.
* **Leak:** `INCOME_GROUP_CODE` places each customer in one of 21 rand bands of the same income (`income_group.csv`). A participant wrote that "if you just subbed the mid of the income bracket for this you'd score around 6k" (skaak, thread 16527, from memory). The best private RMSE was 5,778, and the target's spread is about 9,300 (CatBoost's first iteration in the Pieter-Cawood notebook). So the band carries most of what the models reach. `DATE_LAST_UPDATED` falls in 2022-08 or 2022-09 for 3,415 of the 5,144 customers. In all 5 train rows a notebook prints, it is later than `RECORD_DATE`. Drop the band, as we dropped sdss_17's `redshift` (taken from the measurement that gives the label). With the band kept, the task is close to `Trivial`. To check once the data is loaded: the share of train rows whose band equals the binned target.
* **Label noise:** the target is what the customer declared, not measured income. One participant: "There are some entries where the income bucket and the declared income are not aligned" (Terrence_SHA, thread 15094); another: "Declared Income was never accurate" (thread 15312). How much signal the transactions carry without the band is unknown. Measure it; a small signal is no reason to drop the dataset.
* **Tabular models compete:** the top solutions were CatBoost and bagged extra trees on per-customer transaction aggregates. Seq2seq networks did not help (threads 14806 and 15312).
* **For the definition:** the declaration month lies inside the transaction window. Aggregate each customer's transactions over a window that ends at its `RECORD_DATE`.
* **Access:** there is no public copy of `Train.csv` or `transactions.csv` (searched Kaggle, Hugging Face and GitHub on 2026-10-14). Only `customer.csv`, `income_group.csv` and `employment_status.csv` are public, in the Phosamalebo repo, with Zindi's byte sizes. Zindi needs a login, and the competition was "only open to South African participants"; whether another account can download now is untested. Licence: the Zindi rules forbid redistribution.
* **Ethics and duplicates:** a bank estimating income to offer products, like the credit tasks we keep. Sex and age are features. `absa_corporate_client_activity_forecasting_challenge` is a different dataset (corporate client events), not a duplicate.

---

predict a customer's income based on their transaction history
