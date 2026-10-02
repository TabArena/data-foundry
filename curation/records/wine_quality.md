---
unique_name: wine_quality
name: wine_quality
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2009'
required_split:
- Random (IID)
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=287
- https://doi.org/10.24432/C56S3T
notebook_path: datasets/beyond_iid/old_iid/wine_quality/wine_quality.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/wine_quality/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed by deduplication, split stays IID.** 1,177 of 6,497 rows (18%) are exact copies of another row (all 11 lab values, colour and the median score; 992 sets of up to 8 copies; no set has conflicting scores), so under the random split a row's twin often sits in train. Cortez et al. 2009 (Decision Support Systems 47(4)), Sec. 2.1: the data come from the CVRVV certification system (iLab, May 2004 - February 2007), "Each entry denotes a given test (analytical or sensory)", and the database "was transformed in order to include a distinct wine sample (with all tests) per row"; duplicates are not mentioned. The copies are most likely repeated records from that export, so we drop them (6,497 -> 5,320 rows) instead of grouping, which would only reproduce the deduplication. The paper itself evaluates with 20 runs of random 5-fold CV (Sec. 3) on the data with copies. TabArena v0.1 dataset: results on the old container are not comparable with the deduplicated one.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Originally two datasets with red and white wine. They are diszinguishable by features such as sulfur dioxide. But still unsure whether it makes sense to use them together. Also there are many duplicates, might need to account for that.

Potential issue: Omitted variable bias? Grouped data

Lennart: use UCI version with indicator

Andrej: Add red/white wine indicator

## Reference

Modeling wine preferences by data mining from physicochemical properties
By P. Cortez, A. Cerdeira, Fernando Almeida, Telmo Matos, J. Reis. 2009

Published in Decision Support Systems
