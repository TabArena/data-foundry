---
unique_name: superdatascience_churn_modelling
name: SuperDataScience Churn Modelling
checked_by:
- Lennart
- Andrej
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Duplicate
collections:
- New (BeyondArena)
- TabSTAR
source_links:
- https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling
- https://www.openml.org/search?type=data&id=45062
source_row: 162
type_adapter_id: curation-record-v1
---

## Comments

from https://www.superdatascience.com/deep-learning

Duplicate with Bank_Customer_Churn_Dataset https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset) as we found for TabArena as well

CC (2026-11-04, Andrej): the same course table as bank_customer_churn, retired as generated data on 2026-11-04 (`AHDS` added here): it was drawn by a class-rooted Bayes net (churn first, each column given churn and at most two other columns, tenure, salary and the card flag as noise), which beats every benchmark method on the shipped copy. This copy stays `No`, now for that reason as well as the duplicate.
