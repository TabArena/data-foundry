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
- '?'
source_links:
- https://doi.org/10.24432/C5F88Q
type_adapter_id: curation-record-v1
---

# Online Shoppers Purchasing Intention Dataset

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

## Reference

Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks
By C. O. Sakar, S. Polat, Mete Katircioglu, Yomi Kastro. 2019

Published in Neural computing & applications (Print)
