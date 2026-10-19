---
unique_name: forest_fires
name: forest_fires
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2008'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
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

CC (2026-10-19, Andrej): I disagree with keeping it. The small signal comes from fires on the same day landing in both train and test; for a fire on a new day there is none.

- **Same-day fires straddle the split.** The data has no date, but FFMC, DMC, DC and ISI (the daily values of the Canadian Fire Weather Index, fuel-moisture codes each carried over from the day before) identify the day: 517 fires fall on 227 days, and 78% share their day with another fire. With days kept apart (60 splits), TabPFN-3.5 reaches R^2 -0.002 against the train mean, versus +0.012 on random splits; against shuffled labels (200 shuffles each) p = 0.16, versus p = 0.005 on random splits. The use case (sizing a new fire from that day's weather) never has a training fire from the same day.
- **A split by day is possible**, so the reason given for forcing IID ("a split by time is impossible") does not hold, and under that split nothing is left to learn.
- **The source finds the mean best on RMSE**, our metric: "The best RMSE was attained by the naive mean predictor" (UCI notes on Cortez and Morais 2007).
- **The ranking rewards holding back:** 21 of 29 BeyondArena configurations score below the train mean (median skill -0.003). Beating the mean on most folds is weak evidence: with shuffled labels, TabPFN-3.5 still does so on at least 10 of 12 splits in 11 of 200 shuffles.
- **The day key is inferred**, not given: 9 of the 227 days appear with two weekdays (entry errors or codes carried over). Grouping on the four values keeps them together; a key with month and weekday (236 days) gives the same result (R^2 +0.0003, p = 0.35).

Suggest retiring for no signal under the split the use case needs. Until that is decided, `dataset.py` splits by day (grouped on `fire_day`). forest_fires is the example behind the rule that a small but real signal is no reason to retire (in `task_probes.md` and the curation guidelines); both would need another example.

Cortez P, Morais A. A data mining approach to predict forest fires using meteorological data. In: Neves J, Santos MF, Machado J, eds. New Trends in Artificial Intelligence, Proceedings of the 13th Portuguese Conference on Artificial Intelligence (EPIA 2007). Guimarães: APPIA; 2007:512-523. ISBN 978-989-95618-0-9. Data: UCI Machine Learning Repository, doi:10.24432/C5D88D

## Reference

@article{cortez2007data,
  title={A data mining approach to predict forest fires using meteorological data},
  author={Cortez, Paulo and Morais, An{\'\i}bal de Jesus Raimundo},
  year={2007},
  publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
}
