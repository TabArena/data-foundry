---
unique_name: airfoil_self_noise
name: airfoil_self_noise
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '1989'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=44957
- https://doi.org/10.24432/C5VW2C
notebook_path: datasets/beyond_iid/old_iid/airfoil_self_noise/airfoil_self_noise.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/airfoil_self_noise/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

lab data, prediction of physical systems. Data from a controlled experiment, but there might be confounding factors not covered by the features.

Potential issue: maybe outdated

Lennart: Likely yes, as no objections besides maybe being outdated

Andrej: Outdated, but otherwise fine

CC (2026-10-06, Lennart): Grouped by wind-tunnel run (was IID). The 1,503 rows are 106 runs: one NACA 0012 section (6 chord lengths) at one angle of attack and one free-stream velocity, each a measured one-third-octave spectrum of 8 to 19 bands; the raw file stores each run as one block, and the displacement thickness is constant within a run (computed from its settings). A model is used for a configuration that was not measured, and a measured run comes with its whole spectrum; a random split gave a test row 62% of its run's other bands in train. R^2, 5 x 3 folds, random / grouped by run: extra trees 0.946 / 0.850, LightGBM 0.937 / 0.840, random forest 0.926 / 0.830, kNN-5 0.755 / 0.629, ridge 0.510 / 0.490. The group column `run` is built from chord, angle and velocity (exact, confirmed by the file's blocks); those three stay features. Not grouped by chord length (a new airfoil size is a harder extrapolation). The single-column hidden-group probe missed it: a run is a combination of three columns. Task probes on the build: no flags.

## Reference

Brooks, Thomas F., D. Stuart Pope, and Michael A. Marcolini. Airfoil self-noise and prediction. No. L-16528. 1989.
