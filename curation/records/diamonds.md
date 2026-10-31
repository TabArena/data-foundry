---
unique_name: diamonds
name: diamonds
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
year: '2007'
required_split:
- Random (IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=42225
- https://ggplot2.tidyverse.org
notebook_path: datasets/beyond_iid/old_iid/diamonds/diamonds.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/diamonds/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Depending on what the actual task is, might require temporal split. R2 as metric is not representative as all methods perform strong on R2 for this dataset; potential temporal confounder but only the target is time-related if at all, newer version: https://www.kaggle.com/datasets/hrokrin/the-largest-diamond-dataset-currely-on-kaggle - no source on these dataset include date information but it seems obvious that there might be temporal conneciton, however the task ignores this / does not matter. unclear if the price got adjsuted or computed post hoc

Potential issue: temporal dependence

Lennart: We can likely ignore the impact of time for the task

Andrej: Fulfills requirements

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — a ggplot2 teaching dataset; the source defines no task or score.

CC (2026-10-21, Lennart): diamonds ships the price in dollars and is scored by RMSLE, a metric obvious from the task (new origin `context`: a price's error matters relative to the price).

**Assessment (AI, 2026-10-21):** the price ships on a log scale again (`np.log` in `_clean`, as before today's change) and is scored by RMSLE on the dollar price after the inverse (`Metric.from_context("rmsle", target_transform="log")`, MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 3 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `cut`, `color`, `clarity` (the README lists their levels).

## Reference

Ggplot2: Elegant Graphics for Data Analysis
