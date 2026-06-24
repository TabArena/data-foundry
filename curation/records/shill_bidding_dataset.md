---
unique_name: shill_bidding_dataset
name: Shill Bidding Dataset
checked_by:
- Andrej
suggestion: TBD -> Yes
decision_markers:
- Data Quality Issue
tags:
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: business & marketing
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5Z611
source_row: 605
type_adapter_id: curation-record-v1
---

## Comments

There is no information on which auctions happened during the same time period. There might be data leakage with random splits. Using grouped splits based on auction might be good enough. Some Kaggle notebooks show almost perfect performance with random forest - need to check for leaks carefully. Most features are handcrafted, which again might have introduced issues. According to the paper, statistics from the full dataset (e.g., average number of bids in all the auctions in the dataset) were used. Most other features seem to be generated per bidder. If we split by bidder & auction, the task might be valid. I would add it with grouped splits and then see whether the performance results are suspicious.

## Reference

Alzahrani, A., & Sadaoui, S. (2018). Scraping and preprocessing commercial auction data for fraud classification. arXiv preprint arXiv:1806.00656.
