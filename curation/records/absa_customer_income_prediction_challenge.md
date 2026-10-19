---
unique_name: absa_customer_income_prediction_challenge
name: absa-customer-income-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
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
