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
original_source: Other
year: '1989'
required_split:
- Grouped (NON-IID)
source_links:
- https://ntrs.nasa.gov/citations/19890016302
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

**Assessment (AI, 2026-10-20):** three statements of the CC of 2026-10-06 do not hold (review panel, 2026-10-19). A random 3-fold split puts two thirds (66.6%) of a run's other bands in train; 62.5% is the share of rows whose nearest neighbour is in the same run. Its grouped R^2 values came from a version with the angle numeric; as shipped, with the angle categorical, they were extra trees 0.819, LightGBM 0.813, random forest 0.826. The hidden-group probe did not miss the run because a run is three columns: the thickness alone separates 104 of the 106 runs, and the probe's single-column check skips floats that are not whole numbers (raised in the working copy's REVIEW.md). On "maybe outdated": no rule makes age a reason, and the self-noise of a NACA 0012 section is physics that does not age (kept like concrete_compressive_strength).

CC (2026-10-20, Lennart): Grouped by setup, one chord length at one angle of attack with all its speeds (33 groups; was by run), as the review panel recommended and like concrete_compressive_strength's grouping by mix: under the run split 91.5% of the test runs had their setup in training at another speed. The scaled target is kept as the report's eq. 19 level, named as such. Year 1989 and source the NASA report RP-1218: its Figs. 11-43 plot every measured value (the target and the thickness are its formulas of them), and UCI's 2014 file was digitised from them, so it is a copy (PROV-9 amended). `attack-angle` is numeric now. Rebuild on the curator's ask.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The NASA report builds semi-empirical prediction methods and compares spectra visually; neither it nor the UCI page defines an evaluation metric.

**Assessment (AI, 2026-10-21):** the hidden-group probe now takes float columns (Lennart, 2026-10-21); in that day's sweep the suction-side displacement thickness is a hit (105 values for 106 runs, gap 0.123), next to the known run key. The question raised on 2026-10-20 in the working copy's cross-dataset review is closed.

## Reference

Brooks, Thomas F., D. Stuart Pope, and Michael A. Marcolini. Airfoil self-noise and prediction. NASA Reference Publication 1218 (L-16528), NASA Langley Research Center, 1989. https://ntrs.nasa.gov/citations/19890016302
