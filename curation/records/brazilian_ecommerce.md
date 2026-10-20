---
unique_name: brazilian_ecommerce
name: brazilian-ecommerce/
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data
v2_path: datasets/_dev/tabarena-v0pt2/brazilian_ecommerce/dataset.py
source_row: 705
type_adapter_id: curation-record-v1
---

## Comments

Data seems to be from a real company (Olist), a previous version even was classified. Possible tasks: predict future sales, optimize delivery times.
Multiple tables, requires feature engineering.
Uploaders commit to answering questions (awesome!)
Contains text fields (reviews)

**Assessment (AI, 2026-10-07):** Added as delivery time at checkout: log days from purchase to delivery (regression), with Olist's promised date as a feature and monthly temporal windows (March-July 2018). The data card suggests delivery performance; the uploader's own notebook frames review score instead, predicted from order data "up to delivery phase" (kaggle.com/code/andresionek/predicting-customer-satisfaction, 2018-10-24), the open alternative. Olist released "a simple random sample of all orders that received a customer review" (Kaggle discussion 66466); the last survey was sent on 2018-08-31, so August 2018 orders lost their slow deliveries and are cut. First published on Kaggle 2018-09-21 (the record says 2019). Licence: CC BY-NC-SA 4.0 (Kaggle card).

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run) as implemented: the delivery time promised at checkout is the use case (a late-delivery flag would be a variant of it, the review score a satisfaction task); the one-month gap keeps the labels a refit would have; Olist's promised date stays an input known at checkout; the selection on answered reviews stays an anomaly note.

## Reference

?
