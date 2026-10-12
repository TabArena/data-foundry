---
unique_name: qsar_bioconcentration
name: QSAR_BIOCONCENTRATION
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- New IID
- Free Text (Short)
collections:
- TabSTAR
original_source: UCI
year: '2016'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C56S46
- https://www.kaggle.com/datasets/ishandutta/qsar-bioconcentration-classes-data-set
- https://michem.unimib.it/download/data/
v2_path: datasets/_dev/tabarena-v0pt2/qsar_bioconcentration/dataset.py
source_row: 683
type_adapter_id: curation-record-v1
---

## Comments

Need to understand if class or regression target should be used and how they differ

Contains SMILES string that might need preprocessing in some expert way, or we drop as done by prior work

Data in paper sounds very different to data we have from Kaggle/UCI. We only have the version after feature selection

Super hard to parse if the dataset could be used but I think we can train a model to do so. Might still have problems and result in leaks but worth including for now

**Assessment (AI, 2026-10-07):** Added as the 3-class task of UCI 510 (458 / 64 / 254 chemicals). The class is read from logBCF and the experimental logKOW (Env. Int. SI Sec. 1); an inferred band of ±0.5 log units around the TGD line reproduces 600 of 607 classes with logKOW ≥ 1. So logBCF is dropped, and no descriptor completes the rule. The 779 are the chemicals of the 2015 table (1,056) with an experimental KOW. Benzene/cyclohexane, naphthalene/tetralin and chlorobenzene/chlorocyclohexane carry each other's SMILES and descriptors: swapped back (2015 SI table); triticonazole and two dioxins dropped. SMILES kept as a string. Alternative target: logBCF regression (random forest R² 0.72).

## Reference

@article{grisoni2016investigating,
  title={Investigating the mechanisms of bioconcentration through QSAR classification trees},
  author={Grisoni, Francesca and Consonni, Viviana and Vighi, Marco and Villa, Sara and Todeschini, Roberto},
  journal={Environment international},
  volume={88},
  pages={198--205},
  year={2016},
  publisher={Elsevier}
}
