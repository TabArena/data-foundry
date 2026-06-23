---
unique_name: real_estate_valuation
name: Real Estate Valuation
checked_by:
- Lennart
- Andrej
data_foundry_status: 'Yes'
suggestion: 'No'
tags:
- Tiny Data
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: UCI
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/477/real+estate+valuation+data+set
- https://doi.org/10.24432/C5J30W
source_row: 6
type_adapter_id: curation-record-v1
---

# Real Estate Valuation

## Comments

Small data, unsure time horizon, need to get square foot book to the model

AT: Only 8 time stamps. Also target does not meaningfully vary over time. Rather an IID task. But most importantly, a small dataset like this does not represent real estate prediction

## Reference

@article{yeh2018building,
  title={Building real estate valuation models with comparative approach through case-based reasoning},
  author={Yeh, I-Cheng and Hsu, Tzu-Kuang},
  journal={Applied Soft Computing},
  volume={65},
  pages={260--271},
  year={2018},
  publisher={Elsevier}
}
