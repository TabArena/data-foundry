---
unique_name: clock_protein_toxicity
name: Toxicity
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- New IID
- Many features
- Tiny Data
collections:
- FS Benchmark
original_source: UCI
year: '2021'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
- Scientific Discovery
data_modality:
- Tabular
original_data_state: One Table
source_links:
- 10.24432/C59313
- https://www.openml.org/d/46855
source_row: 1031
type_adapter_id: curation-record-v1
---

# Toxicity

## Comments

Same source as clock_protein_period

The original paper even comes with feature selection. Have to use data.csv file

## Reference

@article{gul2021structure,
  title={Structure-based design and classifications of small molecules regulating the circadian rhythm period},
  author={Gul, Seref and Rahim, Fatih and Isin, Safak and Yilmaz, Fatma and Ozturk, Nuri and Turkay, Metin and Kavakli, Ibrahim Halil},
  journal={Scientific reports},
  volume={11},
  number={1},
  pages={18510},
  year={2021},
  publisher={Nature Publishing Group UK London}
}
