---
unique_name: pancreatic_cancer_mouse_detection
name: NCI Pancreatic
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Many features
- Non-IID (Grouped)
collections:
- FS Benchmark
original_source: Other
year: '2003'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://home.ccr.cancer.gov/ncifdaproteomics/CancerCellPanINDataBinned.zip
- https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp
notebook_path: datasets/beyond_iid/grouped/pancreatic_cancer_mouse_detection/pancreatic_cancer_mouse_detection.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/pancreatic_cancer_mouse_detection/dataset.py
source_row: 1035
type_adapter_id: curation-record-v1
---

## Comments

Original data is multiple serums collected per mouse

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid tiny, high-dimensional task after the task-probe review (flag `unstable`). Grouped by mouse, each test fold holds about 12 PanIN and 13 control mice. The signal is weak but real: on BeyondArena RealTabPFN-2.5 (ROC AUC 0.664), EXAONE (0.654) and TabSwift (0.628) beat 0.5 on all 11 of their folds, while the median of 29 configurations is 0.54 (gradient-boosted trees near chance). Open question, the one that could make this a batch-effect case like prostate_cancer_detection (same NCI-FDA data bank, retired for processing artefacts; Baggerly et al. 2004 found such artefacts in the program's ovarian spectra): the file names' `t` suffix (42% of control spectra, 30% of PanIN spectra; 37 of the 73 mice have spectra with and without it). Within the controls, `t` spectra separate from the others at ROC AUC 0.67 (logistic model, grouped by mouse); within PanIN they do not (0.45). The suffix alone could explain at most about AUC 0.56 of the label, which reaches 0.63-0.66, so the label signal is not only the suffix; what `t` marks needs the authors.

## Reference

@article{hingorani2003preinvasive,
  title={Preinvasive and invasive ductal pancreatic cancer and its early detection in the mouse},
  author={Hingorani, Sunil R and Petricoin, Emanuel F and Maitra, Anirban and Rajapakse, Vinodh and King, Catrina and Jacobetz, Michael A and Ross, Sally and Conrads, Thomas P and Veenstra, Timothy D and Hitt, Ben A and others},
  journal={Cancer cell},
  volume={4},
  number={6},
  pages={437--450},
  year={2003},
  publisher={Elsevier}
}
