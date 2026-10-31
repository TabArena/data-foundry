---
unique_name: jd_com_msom_2020_delivery_time
name: 'JD.com: Transaction-Level Data for the 2020 MSOM Data Driven Research Challenge'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Company
year: '2020'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1287/msom.2020.0900
- https://connect.informs.org/msom/events/datadriven2020
- https://doi.org/10.1287/msom.2023.1209
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: JD.com's own transaction data of March 2018 with order and delivery timestamps, the delivery-time task at checkout that Salari, Liu and Shen (2022) studied on JD data; seven tables to join and access through an INFORMS login.
- Source: Shen, Tang, Wu, Yuan and Zhou, "JD.com: Transaction-Level Data for the 2020 MSOM Data Driven Research Challenge", M&SOM 26(1):2-10 (doi 10.1287/msom.2020.0900; issue of 2024, the data released for the 2020 challenge). As published (abstract): "over 2.5 million customers (457,298 made purchases) and 31,868 SKUs over the month of March in 2018"; seven tables (SKUs, users, clicks, orders, delivery, inventory, network) per the run's assessment, not re-read here (the INFORMS pages answer 403). Target: delivery time of an order or package, arrival minus order time, built from the orders and delivery tables. Access: "use your INFORMS Member ID and Password to access the data" (challenge page, as indexed); no redistribution (EV-4: no verdict reason).
- Use case: JD.com at checkout promises a delivery date from the expected time to arrival (Salari et al. 2022 abstract: "predict the distribution of order delivery time and set promised delivery time to customers in a cost-effective way"); fit direct; regime temporal (orders over 31 days, labels known only on arrival, SPLIT-10).
- Siblings and duplicates: `brazilian_ecommerce` (Yes, Olist delivery time), `delivery_eta` (Yes), `lade_last_mile_delivery_eta`, `meituan_food_delivery_time`, `sendy_logistics_challenge` (TBD -> Yes): other delivery-time data, no duplicate. External collections: none found.
- Better data: found as better data for `brazilian_ecommerce`; no further search this round.
- Papers and pages: the data paper; Allon 2023, introduction to the special section (doi 10.1287/msom.2023.1209); Salari, Liu and Shen 2022, M&SOM 24(3):1421-1436 (doi 10.1287/msom.2022.1081), tree-based distributional forecasts and a cost-sensitive promise rule.
- Metric: none found for the challenge (a research challenge with suggested questions, no leaderboard; challenge page and abstract). Salari et al. score distributional forecasts and a promise policy; their criterion was not read (paywall), so the fallback `rmse` unless it is read and fits (MET-1, MET-5); inputs none.
- Risks for /add-dataset: joins across orders, delivery, users, SKUs and the warehouse network (`Needs extensive data wrangling`); orders split into packages, so one target per order or per package (USE-5); ship-out and station-arrival times come after checkout (LEAK-1); JD's `promise` is known at checkout and stays (USE-6); one month gives few short windows (SPLIT-14, SPLIT-17); the curator downloads with an INFORMS membership.
- Priority: gap 0 (business & marketing, regression, temporal not thin), use case + (Salari et al. name the actor and the promise decision), source + (data paper by JD.com's team), shape + (hundreds of thousands of orders, mixed features, timestamps), risk - (seven tables to join).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `brazilian_ecommerce`.
- as published: over 2.5M customers (457,298 with a purchase) and 31,868 SKUs over March 2018 (paper abstract); 7 tables: orders (order_ID, user_ID, sku_ID, order_date, order_time, quantity, type, promise, original ...; target: delivery time of an order or package: arr_time minus order_time; access: registration (INFORMS member login, MSOM Society membership is paid; no redistribution).
- Why: same task as brazilian_ecommerce (delivery time at checkout): same target, and features of the same kind known at checkout (JD's promised days 'promise' as Olist's promised date, origin and destination warehouse, customer city level, product, price and discounts). Salari, Liu and Shen 2022 (M&SOM, 'Real-Time Delivery ...
- Adds: a company's own release with a data paper, hundreds of thousands of orders in one month against Olist's ~96k delivered orders over two years, and warehouse-to-station-to-door timestamps; only one month (2018-03), so temporal windows are short. Access is the main issue: MSOM members only, and the challenge terms keep ...
