---
unique_name: us_airline_passenger_satisfaction
name: US Airline Passenger Satisfaction
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
tags:
- Larger IID Data
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2018'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/johndddddd/customer-satisfaction
source_row: 505
type_adapter_id: curation-record-v1
---

## Comments

Cleaned version: https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction?select=train.csv

Survey data, but prediction task seems very reasonable

Without source information the data might be fake

The data looks real, but then also a bit too equally distributed everything. Moreover source from Excel so less likely generated

CC (2026-10-01, Lennart): This upload's `satisfaction_2015.xlsx` was tested during the leak audit of `customer_satisfaction_in_airline` (retired; details there). The passenger ratings are generated: rating columns are copied from one another within customer segments (e.g. wifi = gate location in 95.2% of 39,191 satisfied loyal business travellers in Business class; 27 segment-pairs of unrelated items agree on more than 90% of rows, against at most 68% in a real airline survey). Only the flight distances and delays look like real US flight records. The second file, `satisfaction.xlsx`, is a manipulated copy of it (misnamed rating columns, replaced distances, rule-based relabelling). The source questions on Kaggle (2018, 25 votes) were never answered. Evidence for a No with AHDS + Missing source information; verdict left to the curator.

## Reference

Kaggle
