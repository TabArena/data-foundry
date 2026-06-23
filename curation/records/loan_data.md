---
unique_name: loan_data
name: Loan Data
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/ethon0426/lending-club-20072020q1?select=Loan_status_2007-2020Q3.gzip
- (IID fallback https://www.kaggle.com/datasets/itssuru/loan-data)
source_row: 55
type_adapter_id: curation-record-v1
---

# Loan Data

## Comments

Duplicate data source as lending_club


LendingClub.com / https://www.lendingclub.com/personal-banking (likely better to use data from the source) -> no, source is down / data closed off

The older version is without a timestamp. Need to investigate newer version
