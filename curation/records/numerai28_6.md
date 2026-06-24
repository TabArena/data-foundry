---
unique_name: numerai28_6
name: numerai28.6
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '2017'
source_links:
- https://www.kaggle.com/datasets/numerai/encrypted-stock-market-data-from-numerai
- https://www.openml.org/search?type=data&id=23517
source_row: 719
type_adapter_id: curation-record-v1
---

## Comments

CC: ""I heard there are many people interested in this dataset. Also, I think there are newer more extensive versions available. However stock market predictions might also be seen as time-series; 
We have roughly 1k unique values per ""numeric"" attribute across the 100k samples. Some weird preprocessing or lag-based behavior might have happened here""

It is stock data, but the decision function we are predicting is independent of the features and thus it is a valid non-iid temporal task

We need to find a version with a timestamp (or treat it as forced IID), but official data or test data from somewhere should be in the future

## Reference

Kaggle
