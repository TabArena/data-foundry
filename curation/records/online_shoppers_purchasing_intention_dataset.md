---
unique_name: online_shoppers_purchasing_intention_dataset
name: Online Shoppers Purchasing Intention Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2018'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5F88Q
notebook_path: datasets/beyond_iid/old_iid/online_shoppers_purchasing_intention_dataset/online_shoppers_purchasing_intention_dataset.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/online_shoppers_purchasing_intention_dataset/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Shopping prediction (also like a recommender system task); special preprocessing to avoid impact of time; sloved with an LSTM; 

available on OpenML

Click stream data. Study title is Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM - so original data was time-series or at least temporal. dataset consists of feature vectors belonging to 12,330 sessions. 

The dataset was formed so that each session would belong to a different user in a 1-year period to avoid any tendency to a specific campaign, special day, user profile, or period. Although there is a temporal component, the task is conceptualized s.t. the samples are iid. However, I am unsure whether the task is conceptualized correctly regarding the delayed target prediction. The features and the target should have a delay - otherwise it is meaningless to predict a purchase after it already happened

Potential issue: Temporal Task?

Lennart: very likely a temporal task and maybe even grouped

Andrej: temporal task, but the features used for the tabular task are time-invariant. If the task was conceptualized correctly, a temporal split is not needed

CC (2026-10-01, Lennart): Leak audit: kept `PageValues`, dropped the February-May sessions instead (12,330 -> 6,875 rows).
- `PageValues` is meant as a historical Google Analytics page metric, "stored in the application database ... and updated automatically at regular intervals", averaged over the pages a session visits (Sakar et al. 2019, Sec. 2.1 and Sec. 3). Used that way it is a valid real-time feature.
- But the data has two regimes. February-May (5,455 rows): all 560 buyers have PageValues > 0, PageValues alone gives AUC 0.974 (LightGBM 0.981, 0.823 without it). June-December (6,875 rows): 370 of 1,348 buyers (27%) have PageValues = 0, PageValues alone gives AUC 0.814 (LightGBM 0.875, 0.739 without it). Most likely the page-value table was computed over the early period, so the early buyers' own purchases credited their pages; the later values behave like the intended historical metric. A change in site tracking could leave a similar pattern, so this is not proven.
- `SpecialDay` is non-zero only in February and May and is dropped as constant.
- Split: IID (required_split set to Random (IID)): each session belongs to a different user sampled over one year (Sec. 2.1) and only the month is known, so a temporal split would mainly test extrapolation to unseen months.

## Reference

Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks
By C. O. Sakar, S. Polat, Mete Katircioglu, Yomi Kastro. 2019

Published in Neural computing & applications (Print)
