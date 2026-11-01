---
unique_name: kdd_cup_09_appetency
name: KDDCup09_appetency
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Anonymized
year: '2009'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1111
notebook_path: datasets/beyond_iid/old_iid/kdd_cup_09_appetency/kdd_cup_09_appetency.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/kdd_cup_09_appetency/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Marketing data to predict the propensity of customers to buy a product. Data has been already preselected, subsampled and maybe also preprocessed.

Potential issue: ? potential user groups

Lennart: No objection, but need to check data for IDs and maybe preprocess (remove some features) following the description

Andrej: Not in TabRepo, but seems like a good task

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (area under the ROC curve), per task; the ranking averaged churn, appetency and up-selling AUC (Guyon et al. 2009, Analysis of the KDD Cup 2009, JMLR W&CP 7; https://kdd.org/kdd-cup/view/kdd-cup-2009).

CC (2026-10-27, Lennart): marker Anonymized, from the AI review of PR #17: the definition carries the Anonymized data tag; Orange released Var1 to Var230 with hidden meanings and scrambled categories, so it cannot be checked that they were known before the purchase (LEAK-32 names this case).
