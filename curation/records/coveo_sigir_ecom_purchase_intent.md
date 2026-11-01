---
unique_name: coveo_sigir_ecom_purchase_intent
name: Coveo SIGIR eCom 2021 Data Challenge dataset (session browsing events with add-to-cart and purchase; purchase-intent task)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Company
year: '2021'
domain: business & marketing
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://arxiv.org/abs/2104.09423
- https://github.com/coveooss/SIGIR-ecom-data-challenge
- https://doi.org/10.1038/s41598-020-73622-y
- https://github.com/coveooss/shopper-intent-prediction-nature-2020
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a real shop's 5M browsing sessions, released for the SIGIR eCom 2021 challenge. Its second task (will the shopper buy the item added to the cart, in this session) is the purchase-intent task of the accepted `online_shoppers_purchasing_intention_dataset`. The session table has to be built from event logs.
- Source: Coveo, SIGIR eCom 2021 Data Challenge: Tagliabue, Greco, Roy et al., "SIGIR 2021 E-Commerce Workshop Data Challenge" (arXiv 2104.09423, April 2021), and the repository `coveooss/SIGIR-ecom-data-challenge` (README and `README_DC_2021.md`, read 2026-10-31). As published: "36M events" in three files. `browsing_train.csv` holds "almost 5M anonymized shopping sessions" (session id hash, event type, product action, product SKU hash, server timestamp, hashed URL); `search_train.csv` "more than 800k search-based interactions"; `sku_to_content.csv` the catalogue (category hash, price bucket, text and image vectors). The timestamps are "shifted by an unspecified amount of weeks". Access is by a form, "for research and educational purposes", which is no criterion (EV-4).
- Use case: the challenge's task: "given a session containing an add-to-cart event for a product X", predict "whether the shopper will buy X or not in that session". The related paper (Requena et al., Sci. Rep. 2020) studies purchase prediction from clickstreams for "realistic industry use cases". The decision the shop takes on the prediction (an in-session incentive, for example) is not named by the source. Fit direct for the session prefix up to the add-to-cart. Regime temporal by session time (how the challenge built its test set was not read).
- Siblings and duplicates: `online_shoppers_purchasing_intention_dataset` (`Yes`, UCI, 12,330 sessions of one year), `online_shoppers_purchase_intention` (`No`, `Duplicate`), `ga_merchandise_store_sessions` (a new record of this run, Google's demo store) and `customer_propensity_to_purchase_dataset` (`No`, AHDS: a fictional site). The challenge's other task, next-item recommendation, stays out (SEL-9). External collections: none found.
- Better data: found as better data for `customer_propensity_to_purchase_dataset` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: arXiv 2104.09423; Requena et al., "Shopper intent prediction from clickstream e-commerce data with minimal browsing information", Scientific Reports (2020), abstract read: k-gram features with a classifier against an LSTM. The challenge leaderboard and top solutions were not read.
- Metric: the challenge scored "a weighted combination of micro-F1 scores at different clicks": at the add-to-cart and 2, 4, 6, 8 and 10 events later, weighted 1.0 to 0.5, on a test set without resampling (`README_DC_2021.md`; MET-4). A one-row-per-session table at the add-to-cart keeps only the first of these points, and micro-F1 over both classes equals accuracy (if that is how it was averaged). MET-2 decides between the competition metric at that point and the fallback `roc_auc`. Inputs none.
- Risks for /add-dataset: the session table must be built from the event log (`Needs extensive data wrangling`), cutting every session at the first add-to-cart so no later event leaks the purchase (LEAK). SKU and URL hashes are ids with high cardinality and no meaning. The catalogue's text and image vectors are embeddings (SEL-12 on vectorized data: judge per column). Times are shifted by an unknown number of weeks; check that the relative order is kept.
- Priority: gap 0 (business and binary not thin), use case 0 (the challenge fixes the prediction point; the source names no decision), source + (challenge paper and the shop vendor's repository), shape + (5M sessions, temporal), risk - (an event log to aggregate).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `customer_propensity_to_purchase_dataset`.
- as published: more than 30M browsing events (36M per the repo), almost 5M sessions in browsing_train.csv, plus 800k+ search interactions and a catalog table (category, price bucket, text and image vectors); event ...; target: whether a session that contains an add-to-cart ends in a purchase of that item (the challenge's intent-prediction task); a plain 'session ends in purchase' ...; access: registration (form about the user and institution, terms accepted; research and educational use).
- Why: same task as customer_propensity_to_purchase_dataset (a visitor's on-site actions, basket adds and checkout views, predict whether they order), from a real shop with a peer-reviewed description (Requena et al. 2020 treat exactly shopper purchase intent from clickstream)
- Adds: real data with a traceable first publication instead of a fictional website, and millions of sessions. Caveats: event logs, so the session table must be built (Needs extensive data wrangling); IDs and URLs hashed; terms restrict use to research and education
