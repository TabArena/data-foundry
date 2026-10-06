---
unique_name: marketing_campaign
name: Marketing_Campaign
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: Kaggle
year: '2014'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign
notebook_path: datasets/beyond_iid/old_iid/marketing_campaign/marketing_campaign.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/marketing_campaign/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

From O. Parr-Rud. Business Analytics Using SAS Enterprise Guide and SAS Enterprise Miner. SAS Institute, 2014. train a predictive model which allows the company to maximize the profit of the next marketing campaign. Predict who will respond to a product/service offer

Potential issue: Artificial

Lennart: Likely a valid predictive task

Andrej: License; Need to check book on how the data was obtained - could be artificial

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag (three untuned families at skill +0.77 to +0.80) does not hold for tuned methods. On BeyondArena the best (TabFM) reaches ROC AUC 0.926 and the median 0.909, with no other method within noise of the best (Kendall's W 0.84).

## Reference

https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign
