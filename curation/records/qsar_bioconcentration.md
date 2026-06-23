---
unique_name: qsar_bioconcentration
name: QSAR_BIOCONCENTRATION
checked_by:
- Lennart
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
source_row: 683
type_adapter_id: curation-record-v1
---

# QSAR_BIOCONCENTRATION

## Comments

Need to understand if class or regression target should be used and how they differ

Contains SMILES string that might need preprocessing in some expert way, or we drop as done by prior work

Data in paper sounds very different to data we have from Kaggle/UCI. We only have the version after feature selection

Super hard to parse if the dataset could be used but I think we can train a model to do so. Might still have problems and result in leaks but worth including for now

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
