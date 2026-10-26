---
unique_name: houses
name: houses
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
year: '1999'
required_split:
- Random (IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=823
- http://lib.stat.cmu.edu/datasets/
notebook_path: datasets/beyond_iid/old_iid/houses/houses.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/houses/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Regression. California Housing data from 1990 likely is outdated. Also we could collect much more data if this would be a real task. In general, likely an interpretability task anyway. Also data was preprocessed in a very special way. As the data is spatial, custom split might be required? TabRepo version of the dataset almost certainly contains a leak.

Potential issue: Outdated, spatial Data, Preprocssed

Lennart: In a task like this, I think it would count as IID as spatial information are not leaking / we can assume to have/get them.

Andrej: non-iid. Currently, we do not include spatial data as non-iid. Might change that. Temporal split required but not possible (see TabRed)

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The paper is a spatial-econometrics estimation paper: it models ln(median house value) by least squares / spatial autoregression and compares fits, without a prediction metric. RMSE on the log target follows from its least-squares setup.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a house value's error matters relative to the value; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

## Reference

Pace and Barry (1997), "Sparse Spatial Autoregressions", Statistics and Probability Letters.
