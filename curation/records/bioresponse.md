---
unique_name: bioresponse
name: Bioresponse
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: Kaggle
year: '2011'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=4134
- https://www.kaggle.com/c/bioresponse
notebook_path: datasets/beyond_iid/old_iid/bioresponse/bioresponse.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/bioresponse/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict a biological response of molecules from their chemical properties. Data already normalized. Otherwise a great dataset (by Boehringer Ingelheim)

Potential issue: maybe the preprocessing

Lennart: no objection

Andrej: Fits criteria

CC (2026-10-19, Lennart): the descriptors are min-max scaled over Kaggle's train and test molecules; kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `log_loss`, the competition's metric (Kaggle API: "Log Loss"; was the default ROC AUC). Needs a rebuild to reach the container.

## Reference

https://www.kaggle.com/c/bioresponse
