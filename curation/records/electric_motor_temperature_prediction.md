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
