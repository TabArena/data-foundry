---
unique_name: house_prices_nominal
name: house_prices_nominal
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Trivial
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '2011'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/house-prices-advanced-regression-techniques
- https://www.openml.org/search?type=data&id=42165&sort=runs&status=active
source_row: 722
type_adapter_id: curation-record-v1
---

## Comments

CC: "Ames, Iowa house prices. 1460 samples, many arbitrary features. year and month when houses were sold is given, thus is a temporal problem as well; HOWEVER, the original kaggle split is not even temporal which makes this a "gap-filling" problem of questional relevance in reality"

Alternative version of the same data: https://www.kaggle.com/datasets/shashanknecrothapa/ames-housing-dataset

## Reference

@article{de2011ames,
  title={Ames, Iowa: Alternative to the Boston housing data as an end of semester regression project},
  author={De Cock, Dean},
  journal={Journal of Statistics Education},
  volume={19},
  number={3},
  year={2011},
  publisher={Taylor \& Francis}
}
