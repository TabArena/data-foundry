---
unique_name: qualitative_bankruptcy
name: Qualitative_Bankruptcy
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Trivial
- Missing source information
tags:
- Tiny Data
collections:
- TabSTAR
original_source: UCI
year: '2003'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C52889
- https://www.openml.org/d/1495
source_row: 118
type_adapter_id: curation-record-v1
---

## Comments

Might be trivial, only categorical

This version of the data has 250 rows.
In the paper, they speak about 772 companies
UCI only has the test data?

"samples collected during the period of 2001 – 2002
from one of the largest commercial banks in Korea"

Targets are human-made decisions by experts at the bank

It seems basic rule mining already gets 100% performance in the paper

Moreover, this also shows 100% performance https://github.com/ParidhiGola/Qualitative_Bankruptcy/blob/master/Qualitative_Bankruptcy_Project3.ipynb

As a result, we deem this dataset to be trivial most likely, besides missing some source information.

## Reference

@article{kim2003discovery,
  title={The discovery of experts' decision rules from qualitative bankruptcy data using genetic algorithms},
  author={Kim, Myoung-Jong and Han, Ingoo},
  journal={Expert Systems with Applications},
  volume={25},
  number={4},
  pages={637--646},
  year={2003},
  publisher={Elsevier}
}
