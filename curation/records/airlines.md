---
unique_name: airlines
name: airlines
checked_by:
- Andrej
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
- Not Representative
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '2009'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://community.amstat.org/jointscsg-section/dataexpo/dataexpo2009
- https://www.openml.org/d/1169
source_row: 617
type_adapter_id: curation-record-v1
---

## Comments

CC: "Requires temporal split. Also better datasets for this task might be available as only 7 features are given; has noisy duplicates; original data has 120 million rows?; used not as a predictive task according to the website? original question was only about if the weather can predict the delays?"

Check with data from: https://www.transtats.bts.gov/
Openml 42728

Could generally be used, but the available features are limited and could be extended with some work

See: Aeolus for better flight delay dataset

Get newer version of data, likely needs more features to be made a good dataset

CC (2026-10-12, Lennart): aeolus (BTS on-time flights 2016-2024 with hourly weather at both airports, a temporal task in the TabArena v0.2 working copy as `aeolus_1m`) covers US flight delays. When this record is processed, decide whether it is a second flight-delay task or a duplicate of aeolus.

CC (2026-10-26, Lennart): "if airlines really has the same source data, mark it as a duplicate".

**Assessment (AI, 2026-10-26):** it does. OpenML 1169 is Ikonomovska's cut of the ASA Data Expo 2009 airline file ("all commercial flights within the USA, from October 1987 to April 2008", about 120 million records), whose data "comes originally from RITA" (Harvard Dataverse doi:10.7910/DVN/HG7NV7), the BTS agency that publishes the Reporting Carrier On-Time Performance table. aeolus (`aeolus_1m`) and its rebuild aeolus_rebuilt take their flights from the same BTS table (2016-2024 and 2023-2024), and predict the same arrival delay from the schedule. So this record is a cut of the same source without a distinct task (PROV-6): `No` + `Duplicate` of aeolus. airlines_depdelay_10m (the same Data Expo file, departure delay minutes) and pnwflights14 (two airports of 2014, the same BTS table) share the source as well.

## Reference

?
