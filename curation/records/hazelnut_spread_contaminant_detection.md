---
unique_name: hazelnut_spread_contaminant_detection
name: Contaminant-detection-in-packaged-cocoa-hazelnut-spread-jars-using-Microwaves-Sensing-and-Machine-Learning-10.0GHz(Urbinati) / hazelnut_spread_contaminant_detection
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Data Quality Issue
original_source: OpenML
year: '2020'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=45538
- https://www.openml.org/search?type=data&status=active&id=45538&sort=runs
notebook_path: datasets/beyond_iid/old_iid/hazelnut_spread_contaminant_detection/hazelnut_spread_contaminant_detection.ipynb
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Retired: the rows are repeated scans of about ten physical set-ups, and the set-up label is not in the released data, so no trustworthy split exists.** Dataset paper: Urbinati et al. 2020 (ISCAS, doi 10.1109/ISCAS45731.2020.9181293), Sec. IV.A, pp. 2-3: "each sample is a jar filled with safflower oil instead of hazelnut-cocoa spread"; six foreign bodies, "For each type of foreign body, 200 samples are measured, changing their position in the jar: in the middle, at the surface, and in the horizontal plane", with ±10° rotations and ±2 cm shifts. So the 1,200 contaminated rows are about 10 contaminant x position set-ups scanned 100-200 times each (matching the OpenML per-type counts); the number of clean jars behind the 1,200 clean rows is not given. Štitić et al. 2024 (IEEE Trans. AgriFood Electron. 2(2), Sec. III) confirm the OpenML files 45536-45540 are the only release (the same jars at five frequencies) and that the authors used a 7-class label (6 contaminants + clean) that the release does not contain (all five files are 0/1). The file order does not follow the set-ups (no change points at the expected boundaries), so they cannot be reconstructed; the audit's 100-row blocks were a guess. Under the random split, consecutive re-scans land on both sides (AUC 0.98 random vs 0.86-0.92 with held-out blocks; leak audit 2026-09-24). Ricci et al. 2021 (JETCAS) is a different, later dataset (1,240 jars on a conveyor belt, 11 frequencies).
**TODO (outreach):** to bring this family back, contact the authors (Luca Urbinati, luca.urbinati@polito.it, OpenML creator; group of Mario R. Casu, Politecnico di Torino) for the per-row contaminant class and position and the number of clean jars. Also ask about the unreleased datasets that could be new candidates: the conveyor-belt dataset of Ricci et al. 2021 (1,240 jars, 9-11 GHz, plus a "New Test Set" with unseen contaminants) and the multiclass data of Štitić et al. 2024.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Classes very balanced due to experimental design. Different versions with different GHz frequencies - so different experiments. Unclear whether this is scientific discovery or predictive task. sounds like a predictive task and tabular too me

Potential issue: maybe matrix-like features?

Lennart: no objection, seems to be a tabular predictive task, but only take one of these at N GHz!

Andrej: Need to decide which version to include if any

## Reference

@inproceedings{urbinati2020machine,
  title={A Machine-Learning Based Microwave Sensing Approach to Food Contaminant Detection},
  author={Urbinati, Luca and Ricci, Marco and Turvani, Giovanna and Vasquez, Jorge A. Tobon and Vipiana, Francesca and Casu, Mario R.},
  booktitle={2020 IEEE International Symposium on Circuits and Systems (ISCAS)},
  pages={1--5},
  year={2020},
  doi={10.1109/ISCAS45731.2020.9181293}
}

Follow-ups (not this dataset's source): M. Ricci et al., "Machine-learning-based microwave sensing: A case study for the food industry," IEEE JETCAS 11(3):503-514, 2021 (a different conveyor-belt dataset); B. Štitić et al., "Enhanced Machine-Learning Flow for Microwave-Sensing Systems for Contaminant Detection in Food," IEEE Trans. AgriFood Electronics 2(2):181-189, 2024 (states the OpenML release).
