---
unique_name: bias_correction_r_bias_correction_r_2
name: Bias_correction_r/Bias_correction_r_2
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- Multi-target
collections:
- TabArena Reject
original_source: UCI
year: '2020'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.24432/C59K76
v2_path: datasets/_dev/tabarena-v0pt2/bias_correction_r_bias_correction_r_2/dataset.py
source_row: 739
type_adapter_id: curation-record-v1
---

## Comments

CC: "2 targets. Target is to predict the next-day minimum/maximum air temperature for bias correction. Needs temporal split - although the features themselves are time-invariant, the samples are non-iid"

bias correction in numerical weather prediction (NWP) seems to be a whole research field. Therefore, this is a valid task.

Has two targets: predict min and max temperature of a day. Not sure if it makes sense to use only one

**Assessment (AI, 2026-10-07):** Valid task, added with target `Next_Tmin`. A v2 task holds one target; TALENT's `Bias_correction_r` is `Next_Tmax` and `_r_2` is `Next_Tmin`. On 9 weekly windows of summer 2017, the mean of untuned CatBoost, LightGBM and ridge (RMSE 0.78) beats a per-station MOS of the LDAPS forecast (0.82) on 7 of 9 windows. For `Next_Tmax`, MOS on the forecast alone (1.58) beats every untuned model. The split must be temporal: the 25 stations of a day share its weather (LightGBM RMSE 0.62 on random folds, 1.00 with each day kept together). Prediction point: the evening, once the LDAPS run started at 21 KST is out (Cho et al. 2020, Sec. 2.2-2.3).

CC (2026-10-15, Lennart): The task corrects the LDAPS forecast; without one there is nothing to correct, so the three days without an LDAPS run are dropped (review page, issue 4).

**Assessment (AI, 2026-10-15):** 75 station-days dropped (2013-08-10, 2016-07-31, 2016-08-20, all on the training side; 7,648 rows remain). On the shipped windows the mean of untuned CatBoost, LightGBM and ridge still beats per-station MOS on forecast and present-day minimum on 7 of 9 windows (RMSE 0.785 against 0.823, paired SE 0.022).

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run).

## Reference

Cho, D., Yoo, C., & Im, J. (2020). Comparative Assessment of Various Machine Learning-Based Bias Correction Methods for Numerical Weather Prediction Model Forecasts of Extreme Air Temperatures in Urban Areas. Earth and Space Science, 7(4), e2019EA000740. DOI: 10.1029/2019EA000740.
