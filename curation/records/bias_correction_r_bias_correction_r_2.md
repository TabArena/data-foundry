---
unique_name: bias_correction_r_bias_correction_r_2
name: Bias_correction_r/Bias_correction_r_2
checked_by:
- Andrej
data_foundry_status:
- 'DF: WIP'
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
source_row: 739
type_adapter_id: curation-record-v1
---

# Bias_correction_r/Bias_correction_r_2

## Comments

CC: "2 targets. Target is to predict the next-day minimum/maximum air temperature for bias correction. Needs temporal split - although the features themselves are time-invariant, the samples are non-iid"

bias correction in numerical weather prediction (NWP) seems to be a whole research field. Therefore, this is a valid task.

Has two targets: predict min and max temperature of a day. Not sure if it makes sense to use only one

## Reference

Cho, D., Yoo, C., & Im, J. (2020). Comparative Assessment of Various Machine Learning-Based Bias Correction Methods for Numerical Weather Prediction Model Forecasts of Extreme Air Temperatures in Urban Areas. Earth and Space Science, 7(4), e2019EA000740. DOI: 10.1029/2019EA000740.
