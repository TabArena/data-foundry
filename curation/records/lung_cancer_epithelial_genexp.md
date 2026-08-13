---
unique_name: lung_cancer_epithelial_genexp
name: SMK_CAN_187
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Many features
collections:
- FS Benchmark
original_source: OpenML
year: '2007'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/45100
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115
notebook_path: datasets/beyond_iid/new_iid/lung_cancer_epithelial_genexp/lung_cancer_epithelial_genexp.ipynb
source_row: 1038
type_adapter_id: curation-record-v1
---

## Comments

CC: "Dominika: gene-expression profiles from Affymetrix HG-U133A microarrays. Need to check whether it's different from the Lung dataset."

OpenML Rel: https://arxiv.org/abs/2311.12879

Use NCBI source.

Version from NCBI has more columns than on OpenML.

## Reference

@article{spira2007airway,
  title={Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer},
  author={Spira, Avrum and Beane, Jennifer E and Shah, Vishal and Steiling, Katrina and Liu, Gang and Schembri, Frank and Gilman, Sean and Dumas, Yves-Martine and Calner, Paul and Sebastiani, Paola and others},
  journal={Nature medicine},
  volume={13},
  number={3},
  pages={361--366},
  year={2007},
  publisher={Nature Publishing Group US New York}
}
