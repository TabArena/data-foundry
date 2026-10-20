---
unique_name: fraud_detection_in_electricity_and_gas_consumption
name: fraud-detection-in-electricity-and-gas-consumption-challenge
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Review Prio 1 (Atlas)
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2020'
domain: industry & manufacturing
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- '# canonical: permanently-open knowledge competition, no participation restriction'
- https://zindi.africa/competitions/fraud-detection-in-electricity-and-gas-consumption-challenge
- '# students only, 28-29 May 2022'
- https://zindi.africa/competitions/fraud-detection-in-electricity-and-gas-consumption-issea/data
- '# re-runs, all private hackathons on the same data'
- https://zindi.africa/competitions/instadeep-fraud-detection-in-electricity-and-gas-consumption-challenge
- https://zindi.africa/hackathons/cameroon-fraud-detection-in-electricity-and-gas-consumption-challenge
- https://zindi.africa/competitions/indabax-cameroon-2021-2
- https://zindi.africa/competitions/indabax-sudan-classification2022
- https://zindi.africa/competitions/indabax-drc-2022
v2_path: datasets/_dev/tabarena-v0pt2/fraud_detection_in_electricity_and_gas_consumption_1m/dataset.py
source_row: 988
type_adapter_id: curation-record-v1
---

## Comments

AI Summary:
STEG (Société Tunisienne de l'Électricité et du Gaz) electricity & gas consumption fraud detection (Zindi). Real utility billing data: a client table plus an invoice/consumption-history table (~4.5M invoice rows over ~135K clients) to be joined; the target (fraud) is one binary label per client, so the natural split is grouped by client. Invoices carry dates, so a temporal element exists too — worth checking whether a temporal or grouped split better mirrors the real task. Real, sizeable, clear predictive task → looks worth pursuing for the 1M–10M-row benchmark, pending a data inspection.

Tutorial: https://zindi.world/learn/fraud-detection-in-electricity-and-gas-consumption-challenge-tutorial


Lennart:
Train data starts from 2005, release date is 2020, cut-off likely 2019


The competition split uses a grouped split on clients, carrying the same range. Hence this should be a grouped split as well. 

Label-per-group cases, which would be much smaller if we aggregate the columns.

**Assessment (AI, 2026-10-07):** Added as `fraud_detection_in_electricity_and_gas_consumption_1m`. One prediction per
client, grouped by client, from its invoices before 2013-01-01: 83,874 clients billed before and after that date. The
data place STEG's findings in 2013-2019. Clients who left earlier are almost never fraud (21 of 19,133). Meter
replacements, counter status 5 and new counter codes first seen from 2013Q1 go with 21-36% fraud, against 4-12% up to
2012Q4. 47.8% of frauds carry such a trace, which the full history (Zindi's task) leaks. Per-client AUC is 0.61-0.69
with the cut and 0.85 with the full history. First run as AI Hack Tunisia #4 (Sep 2019). `indabax_drc_2022` is the
same STEG data.

## Reference

Zindi main source
