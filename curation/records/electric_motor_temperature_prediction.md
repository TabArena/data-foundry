---
unique_name: electric_motor_temperature_prediction
name: ElectricMotorTemperature
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Regression)
tags:
- Non-IID (Grouped)
- Multi-target
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2021'
domain: industry & manufacturing
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature
notebook_path: datasets/beyond_iid/grouped/electric_motor_temperature_prediction/electric_motor_temperature_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/electric_motor_temperature_prediction/dataset.py
source_row: 700
type_adapter_id: curation-record-v1
---

## Comments

CC: ""Signal/time-stream data with groups of sessions, likely needs a group-based split based on `profile_id`; unsure about temporal splits as it would be all from the same time at once, or one needs to set time diff per session

add coolant temperature outlier feature, u_d, motor speed; resolve qd coordinates?
could create three datasets from the three targets; need to remove other target to avoid leakage otherwise (likely torque bad, others two okay, pm best)""

Related link: https://www.kaggle.com/datasets/graxlmaxl/identifying-the-physics-behind-an-electric-motor



See Table 2 in paper for what is measured input and what is measured target (https://ieeexplore.ieee.org/abstract/document/9296842)

Text says 4 target temperatures? are 4 PM, ST, SW, SY, we select PM

CC (2026-10-06, Lennart): Kept after the task-probe sweep of the 2026-10-06 build. The probe flagged `no_spread`: R^2 0.970 (linear), 0.963 (LightGBM) and 0.937 (random forest), and with 3 grouped folds the paired gap (0.026) is within 2 standard errors. The tuned methods spread: on BeyondArena the RMSE of the 21 configurations ranges from 1.77 (RealMLP, tuned) to 3.52 (dummy 22.9), so the task separates methods even though all explain most of the variance.

## Reference

@article{kirchgassner2020estimating,
  title={Estimating electric motor temperatures with deep residual machine learning},
  author={Kirchg{\"a}ssner, Wilhelm and Wallscheid, Oliver and B{\"o}cker, Joachim},
  journal={IEEE Transactions on Power Electronics},
  volume={36},
  number={7},
  pages={7480--7488},
  year={2020},
  publisher={IEEE}
}
