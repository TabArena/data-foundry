---
unique_name: mental_health_tech
name: MENTAL_HEALTH_TECH
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- New IID
- Free Text (Sentences)
collections:
- TabSTAR
source_links:
- https://www.openml.org/search?type=data&id=46719
- https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
source_row: 532
type_adapter_id: curation-record-v1
---

## Comments

Contains one comment column that is empty 87% of the time. Most of the comments are not super relevant compared to the rest of the survey. If we filter to those with good comments, we end up with almost no data. So we can skip this data for now.

Contains some cases with comments (but mostly empty); so not fully text.

Clearly survey data, no ground truth or objective target from just the survey data. So unclear how to create a predictive task.
