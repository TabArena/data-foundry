---
unique_name: superconductivity
name: superconductivity
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
- https://www.openml.org/search?type=data&id=44964
- https://doi.org/10.24432/C53P47
notebook_path: datasets/beyond_iid/old_iid/superconductivity/superconductivity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/superconductivity/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

recent and likely still useful predictive task but I am missing domain knowledge

 Talent uses UCI version. Initially, custom train/test split. Task: Predict critical temperature. Might require some special split based on molecules.Paper uses a random split 2/3 - but might be wrong. Data was preprocessed already. Moreover, there is an additional file with information about the molecules.

Potential issue: -

Lennart: No objection

Andrej: But need to check for leaks after obtaining results due to split & preprocessing.

CC (2026-10-06, Lennart): Grouped by composition (was IID). The split follows what the task does in reality: the source predicts the critical temperature from the formula alone, and a model like that is used for compositions without a measured temperature, so a test composition must be new to it. A random split gave 35% of the test rows an identical feature row in train. The key is the composition: each element's share, from the element counts in `unique_m.csv` (shipped with the release, row-aligned with `train.csv`, same temperatures), compared at 6 decimals, which only removes floating-point noise (5 to 8 decimals give the same 15,164 compositions; 4 decimals would merge 28 different ones). It joins formulas that write one composition differently (`Dy1Ir2Rh2B4` and `Dy1Rh2Ir2B4`, `V2Zr1` and `V66.6Zr33.3`), which a key on the formula string would split; no set of identical feature rows lies in two groups. 2,422 compositions have 2 to 110 entries (6,099 repeated rows); their temperatures differ by a median standard deviation of 1.3 K and by more than 30 K for 132, likely other samples, phases or pressures, which the release does not record, so one composition can hide several materials that no model on these features can tell apart. Every entry is kept and scored per row. Not grouped by element set (R^2 on log1p(Tc) 0.913 random, 0.899 by composition, 0.845 by element set): a new composition is usually another proportion of known elements, not a new family; Meredig et al. (2018) study the new-family case. Not deduplicated: Stanev et al. (2018) average a material's entries when their standard deviation is below 5 K and drop the rest (76% of our repeated compositions would be averaged); we keep the release's rows. The cost of grouping is small but real: R^2 on Tc random / grouped, 2 x 3 folds: extra trees 0.921 / 0.919, random forest 0.919 / 0.910, LightGBM 0.916 / 0.913, kNN-5 0.890 / 0.883, ridge 0.735 / 0.732. Its size did not decide: the use case did. Task probes on the build: no flags.

## Reference

Hamidieh, Kam. "A data-driven statistical model for predicting the critical temperature of a superconductor." Computational Materials Science 154 (2018): 346-354.
