---
unique_name: molecularproperties
name: molecularproperties
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Wrong Domain / Source Modality
tags:
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/competitions/champs-scalar-coupling/data?select=train.csv
- https://doi.org/10.1371/journal.pone.0253612
- https://osf.io/kcaht
- https://github.com/larsbratholm/champs_kaggle
source_row: 534
type_adapter_id: curation-record-v1
---

## Comments

CC: "Can pre-filter data according to existing molecules, requires expert feature engineering to even find predictive signal from molecular structures but has some un-engineered data we could use/join; target is made up of combination of targets"


Solutions were very custom NN models, not tabular. Might be solvable by tabular, but requires custom preprocessing and is unclear

CC (2026-09-23, Lennart): **No.** Reasons: (1) every value is DFT-computed, not measured, i.e. simulated data with a dedicated benchmark community (criterion 4B, as `higgs`); (2) it is a 3D molecular-graph task where tabular models are not competitive and the tabular file alone carries no signal (criterion 4A); the non-commercial licence (CC-NC-BY 4.0) is noted, not a factor. This settles the "unclear" in the note above. What it is: the Kaggle CHAMPS competition (2019), written up by its organisers in Bratholm et al., PLOS One 16(7):e0253612, 2021. Molecules are QM9 ("~134k molecules comprised of carbon, fluorine, nitrogen, oxygen and hydrogen", at most 9 heavy atoms) and the target is a DFT-computed NMR coupling per atom pair: "using the B3LYP functional and the 6-31g(2df,p) basis set to compute NMR parameters on the optimized QM9 structures". Nothing in it is measured, so criterion 4B applies as for `higgs`, and QM9 is the standard molecular-ML benchmark, so dedicated benchmarks exist. The "combination of targets" in the old comment is the FC + SD + PSO + DSO breakdown of the coupling, shipped for train only (no leak).

Modality: the tabular file (molecule, two atom indices, coupling type) has no signal without the XYZ geometry, and "All of the prize winning teams utilized deep neural networks where the encoder learned the pair-feature vectors from the coordinates, atom types, distances, etc." A hand-engineered XGBoost (EDeanF/Kaggle_CHAMPS README: through-bond and through-space distances, angles, hybridisation) reached LMAE -1.06, rank 1307 of 2700+, against a top of about -3.2 (0.039 Hz geometric mean error), so tabular models are not competitive (4A). Split: "65% of molecules in the dataset were randomly partitioned into a training set and the other 35% to a testing set", i.e. grouped by molecule, tag correct. Licence: "The computed QM9 scalar coupling constants are available under Creative Commons CC-NC-BY 4.0" (non-commercial); data at osf.io/kcaht and github.com/larsbratholm/champs_kaggle, which notes a symmetry error corrected after the competition. Kaggle discussion threads not read (page not fetchable).
