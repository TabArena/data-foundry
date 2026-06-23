---
unique_name: myocardial_infarction_complications
name: Myocardial infarction complications
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- New IID
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- 10.24432/C53P5M
source_row: 668
type_adapter_id: curation-record-v1
---

# Myocardial infarction complications

## Comments

Has multiple datasets / outcomes in one. Take one at most. Moreover, clearly describes which time points we could simulate with the data.

hard to decide for one target. All of them have some merit. According to Dr. ChatGPT, it is better to model some of the Arrhythmias related cases and avoid the leathal outcome. Make judgement call based on data

## Reference

@article{golovenkin2020trajectories,
  title={Trajectories, bifurcations, and pseudo-time in large clinical datasets: applications to myocardial infarction and diabetes data},
  author={Golovenkin, Sergey E and Bac, Jonathan and Chervov, Alexander and Mirkes, Evgeny M and Orlova, Yuliya V and Barillot, Emmanuel and Gorban, Alexander N and Zinovyev, Andrei},
  journal={GigaScience},
  volume={9},
  number={11},
  pages={giaa128},
  year={2020},
  publisher={Oxford University Press}
}
