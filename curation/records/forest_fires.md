---
unique_name: forest_fires
name: forest_fires
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2008'
domain: environmental science & climate
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D88D
- https://www.kaggle.com/datasets/elikplim/forest-fires-data-set
- https://www.openml.org/search?type=data&id=44962
notebook_path: datasets/beyond_iid/new_iid/forest_fires/forest_fires.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/forest_fires/dataset.py
source_row: 748
type_adapter_id: curation-record-v1
---

## Comments

CC: "Data from forest fires, used ln(x+1) target scaling; time invariant features,"

Has spatial data (x,y) and temporal (month/day). Need to see how to split the data for a real task. Spatial data represents a square on a map

Paper used default cross-validation, which makes not a lot of sense given the data/task but given their setup and goal it makes sense

"further research is needed to confirm if
direct weather conditions are preferable than accumulated values, as suggested by this
study"

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid task after the task-probe review. The probe flagged `no_signal` (the untuned linear model, random forest and LightGBM all score below the train mean), but tuned methods find a small, consistent signal: on BeyondArena, TabPFN-3.5 reaches RMSE 1.390 on `log1p(area)` against 1.399 for the train mean (R^2 0.013) and beats the mean on 26 of 32 folds, TabDPT on 43 of 60, while random forest, ExtraTrees and LimiX-2 lose to the mean on almost every fold. 48% of the fires burned 0 ha; knowing which ones would give R^2 0.58, but whether a fire burns more than 0 ha is predicted at ROC AUC 0.51-0.58 and the size of a burned fire not at all (R^2 below 0 against the burned fires' mean), so a hurdle model (P(area > 0) times the expected log area of a burned fire) reaches R^2 0.002 on the 60 shipped splits. A small signal is not a reason to retire; the ranking on this dataset mostly rewards methods that do not overfit noise.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source mae — Cortez & Morais 2007 rank models by MAD of the burned area on the raw scale (RMSE also reported); the target now ships in hectares, the log1p transform is dropped (MET-3, MET-5). Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** the burned area ships on a log1p scale again (`np.log1p`, as before today's change, the authors' modelling scale) and is scored by MAE on the area in hectares, after the inverse, as Cortez & Morais scored MAD (`Metric.source("mae", target_transform="log1p")`, MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `month` (a partial order); `day` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 calendar or compass cycles ordered.

## Reference

@article{cortez2007data,
  title={A data mining approach to predict forest fires using meteorological data},
  author={Cortez, Paulo and Morais, An{\'\i}bal de Jesus Raimundo},
  year={2007},
  publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
}
