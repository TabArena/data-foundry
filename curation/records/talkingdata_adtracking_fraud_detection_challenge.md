---
unique_name: talkingdata_adtracking_fraud_detection_challenge
name: TalkingData AdTracking Fraud Detection Challenge
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/competitions/talkingdata-adtracking-fraud-detection
source_row: 330
type_adapter_id: curation-record-v1
---

## Comments

Again, high cardinality categoricals IDs and IPs. Needs IP preprocessing; have to remove attribute_time as it is leaking; super imbalanced; many value outliers; requires a lot of custom/expert feature engineering; likely use negative down sampling which would make the datasets much smaller again
