---
unique_name: concrete_compressive_strength
name: concrete_compressive_strength
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2007'
required_split:
- Grouped (NON-IID)
source_links:
- https://www.openml.org/search?type=data&id=44959
- https://doi.org/10.24432/C5PK67
notebook_path: datasets/beyond_iid/old_iid/concrete_compressive_strength/concrete_compressive_strength.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/concrete_compressive_strength/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data from a lab, likely a real problem?

Potential issue: unclear domain task

Lennart: Likely yes as no objects beside maybe outdated / lab setup that is not a real predictive task

Andrej: Seems fine

**Assessment (AI, 2026-10-14):** Hidden groups. The 1,030 tests are 428 concrete mixes (identical amounts of all seven ingredients); 182 mixes are tested at several ages (up to 20 tests), so 76% of the rows share their mix with another row, and the mixes carry 65% of the strength variance. On the shipped random splits (10 x 3), 73% of the test rows had their mix in training at another age. R^2, random against grouped by mix: LightGBM 0.925 / 0.874, extra trees 0.912 / 0.881, random forest 0.901 / 0.856, MLP 0.916 / 0.838, kNN 0.882 / 0.826, ridge 0.816 / 0.804; the ranking of the models changes. The use case, designing a new mix (the UCI page lists Yeh 1999, "Design of High Performance Concrete Mixture Using Neural Networks"), predicts for a mix not tested before. The hidden-group probe missed it because it only tests single columns (the ingredient amounts are fractional, so none is a candidate, and Age has 14 values) and its near copies need at least 10 informative columns (the table has 8). Since 2026-10-14 it also checks keys of all columns but one, and `(all but Age)` is a hit (76.1% of the rows, 0.0% with independent columns; untuned LightGBM R^2 0.923 random against 0.857 grouped). The definition now groups by `mix`, built from the seven ingredient columns and not a feature: 10 x 3 grouped splits, 142-143 test mixes per fold; group_probes.py: LightGBM 0.924 IID against 0.874 grouped, and across mixes ridge 0.596, random forest 0.859, LightGBM 0.876, kNN 0.703. This changes the split shipped in TabArena v0.1 and BeyondArena.

CC (2026-10-14, Lennart): Grouped by mix: a new prediction is for a mix not tested before.

## Reference

Yeh, I-C. "Modeling of strength of high-performance concrete using artificial neural networks." Cement and Concrete research 28.12 (1998): 1797-1808.
