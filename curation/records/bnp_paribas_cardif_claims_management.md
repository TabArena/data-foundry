---
unique_name: bnp_paribas_cardif_claims_management
name: BNP_Paribas_Cardif_Claims_Management
checked_by:
- Lennart
- Andrej
data_foundry_status: Much work
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: Kaggle
year: '2016'
domain: insurance
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/bnp-paribas-cardif-claims-management/overview
source_row: 744
type_adapter_id: curation-record-v1
---

# BNP_Paribas_Cardif_Claims_Management

## Comments

CC: "Competition was won through deanonymizing the features and analyzing them. In doing so the participants were able to find that the data is panel data structured and the target is very dependent on the level. Hence, the task actually requires a temporal (maybe also grouped) split. The leak can be exploited through feature engineering, which CatBoost does automatically. Hence, this dataset has still value for benchmarking as it covers an interesting bias. More information on the winning solution: https://www.kaggle.com/competitions/bnp-paribas-cardif-claims-management/discussion/20247"

Looks good but needs some help with preprocessing and co

The data is anonymized and we cannot recover the original grouped, temporal structure. It might be possible to approximate that by studying the top solutions, but this would be a lot of work

## Reference

Anna Montoya, detoldim, Dumora, Lam Dang, Sebastien Conort, and Will Cukierski. BNP Paribas Cardif Claims Management. https://kaggle.com/competitions/bnp-paribas-cardif-claims-management, 2016. Kaggle.
