---
unique_name: loan_ibrd
name: LOAN_IBRD
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- New IID
- Free Text (Short)
collections:
- TabSTAR
- STRABLE
original_source: GOV Website
year: '2026'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46467
- https://www.worldbank.org/en/who-we-are/ibrd
- https://www.openml.org/search?type=data&status=active&id=46511
- https://financesone.worldbank.org/ibrd-statement-of-loans-and-guarantees-latest-available-snapshot/DS00047
source_row: 603
type_adapter_id: curation-record-v1
---

## Comments

Check if we can get newer version of data from source, yes we can and should take the newest data!

Unsure if this is a reasonable task or not and if one can predict it, needs to see once we look into the data

The data as is might be missing a lot of features that actually drive the predictions. So making this a real task is a lot of work

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ibrd_loans_historical_snapshots` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

## Reference

Website
