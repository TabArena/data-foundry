---
unique_name: huntprohibited
name: huntprohibited
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Free Text (Sentences)
- Non-IID (Temporal)
- Larger IID Data
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2014'
domain: business & marketing
required_split:
- Temporal (NON-IID)
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/avito-prohibited-content/data?select=avito_train.zip
v2_path: datasets/_dev/tabarena-v0pt2/huntprohibited_1m/dataset.py
source_row: 642
type_adapter_id: curation-record-v1
---

## Comments

CC: "Russian text; text to features script exists; free-text categorical in json format, extra leaking column, that could be used to sub-filter data; close_hours leaking test data; some count features from text; likely some problem with malicious users, who one should detect instead of the ads itself"

needs some basic preprocessing as shown by the hosts; non-English language might be a problem for downstream models

**Assessment (AI, 2026-10-07):** The temporal split cannot be built: the file has no date, and the competition admin wrote "The ids have been randomly assigned" (Kaggle discussion 9554); block rate and seasonal words are flat across id deciles. Defined as IID `huntprohibited_1m` (ForcedIIDFromTemporal; 1.5M of 3,963,488 ads after dropping 32,315 duplicates). `close_hours` is post-outcome ("not available at scoring phase", discussion 9729) and `is_proved` exists only for blocked ads; both dropped. With no seller id, sellers cannot be grouped; 1.39% of test ads share a description with a train ad (0.50% of April ads), worth at most 0.002 ROC AUC. Text carries most of the signal (fold 0): structured columns ROC AUC 0.932, TF-IDF text 0.994.

## Reference

Kaggle
