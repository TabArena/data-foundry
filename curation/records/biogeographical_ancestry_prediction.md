---
unique_name: biogeographical_ancestry_prediction
name: Human Genome data
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Tiny Data
- New IID
collections:
- New (BeyondArena)
original_source: Github
year: '2025'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.internationalgenome.org/
- https://www.kaggle.com/datasets/i191796majid/human-genetic-data
- https://www.fsigenetics.com/article/S1872-4973(25)00070-5/fulltext
- https://github.com/CarolaHeinzel/BGA-Classification/blob/main/datat/filtered_population_eur_update.xlsx
source_row: 686
type_adapter_id: curation-record-v1
---

# Human Genome data

## Comments

The Kaggle version already did PCA.

This dataset is very close to the data from one of my collaborations (https://www.sciencedirect.com/science/article/pii/S1872497325000705,https://www.biorxiv.org/content/10.1101/2025.11.08.687358v1.abstract) and we could easily find more similar data / create a real task from it. It comes with different kinds of marker sets. Moreover, some of the default tasks are trivial to solve.

This could give us a "real" dataset with a lot of features.

From going through the project, let us try to use the version from my collaboration. We use the Inter European version as the continental task is the "simpler" task. Moreover, note that these datasets come with expert-based feature selection.

Basic preprocessing: https://github.com/CarolaHeinzel/BGA-Classification/blob/main/CrossValidation_Code/run_convert_excel_data.py, All data is categorical, target Population

Relevant classes we should have: 09. Russia - Russian        British in England and Scotland        Finnish in Finland        France        Iberian population in Spain        Italy        Turkey        Utah Residents (CEPH) with N & W European ancestry

## Reference

@article{heinzel2025advancing,
  title={Advancing biogeographical ancestry predictions through machine learning},
  author={Heinzel, Carola Sophia and Purucker, Lennart and Hutter, Frank and Pfaffelhuber, Peter},
  journal={Forensic Science International: Genetics},
  volume={79},
  pages={103290},
  year={2025},
  publisher={Elsevier}
}
