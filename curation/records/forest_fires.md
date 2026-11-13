---
unique_name: forest_fires
name: forest_fires
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- No Signal
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
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

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source mae — Cortez & Morais 2007 rank models by MAD of the burned area on the raw scale (RMSE also reported); the target now ships in hectares, the log1p transform is dropped (MET-3, MET-5). Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** the burned area ships on a log1p scale again (`np.log1p`, as before today's change, the authors' modelling scale) and is scored by MAE on the area in hectares, after the inverse, as Cortez & Morais scored MAD (`Metric.source("mae", target_transform="log1p")`, MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends not to ship it. Priority 3: gap +, use case + (the paper states the fire-service use), source +, shape -, risk - (no signal on unseen days; recommended not to ship).
**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `month` (a partial order); `day` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 calendar or compass cycles ordered.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `fpa_fod_attributes_wildfire_size` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Retire: on fire days held out of training, as the use case needs, no model beats a constant, neither TabPFN-3.5 on the log scale (p = 0.16) nor untuned models under the declared MAE in hectares (p = 0.40 to 0.99). Priority 1: gap 0, use case 0, source 1, shape 0, risk -1.

CC (2026-11-05, Andrej): retired (`No (Retired)`, `No Signal`): once the leak between fires of the same day is closed, the burned area is not learnable. The data: 517 forest fires in the Montesinho park, Portugal, 2000-2003 (UCI 162, Cortez and Morais 2007), the burned area from the fire's map square, month, weekday and that day's weather.
- **The signal was the day, not the fire:** the daily fire-weather values identify the day (517 fires on 227 days, 78% sharing their day); on random splits TabPFN-3.5 beats the training mean (R² +0.012, above all 200 shuffles of the labels), with whole days held out it does not (R² -0.002, p = 0.16).
- **On unseen days no model beats a constant under the declared metric:** MAE on the area in hectares; the training median scores 12.75 ha, untuned LightGBM, a random forest and the back-transformed mean of the log area 1.0% to 4.3% worse, and against shuffled targets p = 0.40 to 0.99. The source itself found the mean predictor best on RMSE.
- **Why the keep of 2026-10-06 no longer holds:** it rested on random splits, which the day grouping overturned (CC 2026-10-19).
Marker `No Signal`, as for clock_protein_toxicity. Better data for the task, `fpa_fod_attributes_wildfire_size`, is screened in its own record.

CC (2026-11-11, Lennart): retirement agreed with Andrej, now under step 2 of TP-2 (amended 2026-11-11): the signal on
unseen days is real, but too small to change the use case's decision.
- **A tuned model finds a signal on unseen days:** on day-grouped splits (the day key FFMC|DMC|DC|ISI, 227 days,
  20 x 3 folds, inner validation grouped by day), LightGBM tuned over 50 configurations (L1 objective on the log area)
  beats the training median under the declared MAE in hectares beyond 100 runs of the same pipeline on shuffled
  labels: MAE 12.69 against 12.71 ha (+0.14%), p = 0.02. Early-stopped LightGBM (-0.05%, p = 0.24) and RealMLP
  (-3.0%, p = 0.43) do not. `No Signal` by step 1 does not hold: the evidence of 2026-11-05 rested on untuned models
  and TabPFN-3.5 alone.
- **The gain changes no decision:** the use case sends crews to the fire that will grow large; 0.02 ha (about 200 m²)
  per fire against a typical error of 12.7 ha moves no dispatch. A metric closer to the decision, a ranking of the
  fires of one day, does not fit the data: 115 of the 227 days have one fire and 160 have one or two.
- **The day grouping holds:** of the 112 days with more than one fire, 9 mix weekdays and 2 mix months (random sets of
  the same sizes give about 105 and 98); fires of one day have related areas (p = 0.025); grouping by day halves the
  tuned gain of the random splits (0.29% to 0.14%).
It supersedes the keep of 2026-10-06. Marker `No Signal` (TP-2, step 2).

## Reference

@article{cortez2007data,
  title={A data mining approach to predict forest fires using meteorological data},
  author={Cortez, Paulo and Morais, An{\'\i}bal de Jesus Raimundo},
  year={2007},
  publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
}
