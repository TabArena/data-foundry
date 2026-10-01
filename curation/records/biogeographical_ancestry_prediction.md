---
unique_name: biogeographical_ancestry_prediction
name: Human Genome data
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
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
notebook_path: datasets/beyond_iid/new_iid/biogeographical_ancestry_prediction/biogeographical_ancestry_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/biogeographical_ancestry_prediction/dataset.py
source_row: 686
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Fixed a source artefact: dropped the Turkey class and set no-calls to missing.** The data is Ruiz-Ramirez et al. 2023 (VISAGE Enhanced Tool), Supplementary Table S1A, as used by Heinzel et al. 2025 (Sec. 2.1), which pools 1000 Genomes, HGDP-CEPH, Middle East, SGDP and Estonian Biocentre samples. By sample ID, the inter-European classes come from three sources: 1000 Genomes (HG/NA IDs: British, Finnish, Iberian, Toscani, Utah CEPH), HGDP (HGDP IDs: Russian, Basque, French, Sardinian) and Turkey (IDs 2TR-..., source not confirmed; the Ruiz-Ramirez PDF was not reachable). Turkey's source has an assay artefact: rs3857620 is AG in 24 of 28 samples, 0 AA (about 5 expected under Hardy-Weinberg equilibrium), and GG in all 607 others; with the no-calls it separated Turkey at AUC 0.96-0.98 (leak audit 2026-09-24). Changes: Turkey dropped (635 -> 607 rows, 10 -> 9 classes, a deviation from the paper's ten); rs3857620 and rs367953206 (constant without Turkey) dropped; "NN" no-calls set to missing (28 cells in 24 HGDP rows, none in 1000 Genomes, so a weak source hint remains). Each class still comes from one source; the task stays hard (LightGBM log loss worse than the class prior on the shipped splits). rs2789823 (AG in 7 rows, all Iberian) may be a smaller artefact; kept.

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
