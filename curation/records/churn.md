---
unique_name: churn
name: churn
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
year: '2005'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=40701
notebook_path: datasets/beyond_iid/old_iid/churn/churn.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

5000 sample telephony account churn data. Likely outdated; in the book (old and new eversion) that mentions the original data, it only talks about 3333 samples and a slightly different class ratio; likely the book only used a train split but test split somehow was able to be used by openml

Potential issue: Outdated, source missing

Lennart: source information missing otherwise okay

Andrej: Fits criteria
