---
unique_name: house_prices_nominal
name: house_prices_nominal
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
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
v2_path: datasets/_dev/tabarena-v0pt2/house_prices_nominal/dataset.py
source_row: 722
type_adapter_id: curation-record-v1
---

## Comments

CC: "Ames, Iowa house prices. 1460 samples, many arbitrary features. year and month when houses were sold is given, thus is a temporal problem as well; HOWEVER, the original kaggle split is not even temporal which makes this a "gap-filling" problem of questional relevance in reality"

Alternative version of the same data: https://www.kaggle.com/datasets/shashanknecrothapa/ames-housing-dataset

**Assessment (AI, 2026-10-07):** The Kaggle train.csv (OpenML 42165 / 42563) is a random half of De Cock's JSE
file (https://jse.amstat.org/v19n3/decock/AmesHousing.txt, doi:10.1080/10691898.2011.11889627; 2,930 sales
2006-2010): all 1,460 rows match it in every feature and the price. The mirror of `ames_housing_dataset` equals that
file cell for cell, so its `Duplicate` marker stands. The v2 definition uses De Cock's file (2,919 rows after dropping
the incomplete July 2010 and his three partial-sale outliers), the log price and 13 two-month temporal windows.
`Trivial` is not borne out: the mean price per `Overall Qual` grade is worse than LightGBM in all 13 windows (RMSE
0.228 against 0.119). Licence: JSE allows teaching use; publications need the author's consent.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Well-documented Ames sales as a temporal regression on the full file; solid but another house-price task in a crowded domain.

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
