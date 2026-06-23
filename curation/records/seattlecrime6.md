---
unique_name: seattlecrime6
name: seattlecrime6
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Ethical Issue
- No Good Target  / Scientific Discovery
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
year: '2019'
source_links:
- openml 41960
- https://data.seattle.gov/Public-Safety/Crime-Data/4fs7-3vj5 - 24-06-2019
source_row: 542
type_adapter_id: curation-record-v1
---

# seattlecrime6

## Comments

CC: "Might require temporal split, 144 classes as target. Note thar grinsztajn uses wrong target from another study. Might require preprocessing and leaving out some features which would not be available at inference time in the real task. also in reality more features might be available; predicting crime type based on time and location might be a weird task "

Features in OpenML version do not conceptualize a task. All of them would be know when the target is known, or leak the target even. Otherwise, it might be a forecasting task too. Also, target might be multiple in some way or form.

Could be forecasting / predicting just based on time if there will be crime somewhere? 

Grouped data where one report might have multiple offenses. Contains redacted data.

Very unclear how to build a real predictive task from this and with what goal and if it would be ethical nice (and not just a biased model)
