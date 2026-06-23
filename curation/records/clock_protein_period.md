---
unique_name: clock_protein_period
name: Period Changer
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Too Small
tags:
- Many features
- Tiny Data
- New IID
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
- 10.24432/C5B31D
source_row: 1030
type_adapter_id: curation-record-v1
---

# Period Changer

## Comments

Same source as clock_protein_toxicity


Onlyt has 90 samples, not enough for us here.
Plus, it is the same sourec data (not target) as Toxicity. So we keep only Toxicity

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
