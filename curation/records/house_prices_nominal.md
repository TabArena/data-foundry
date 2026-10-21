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
- https://jse.amstat.org/v19n3/decock/AmesHousing.txt
- https://doi.org/10.1080/10691898.2011.11889627
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

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes. For the curator (REVIEW.md issues 7, 4, 3, 9, 10): drop the 82 Family, Alloca and AdjLand sales by USE-5 (34 of them scored; mean scored RMSE -0.0051, SE 0.0029, lower in 8 of 13 windows); keep no gap as an exception to SPLIT-10 that rests on the mechanism (the short June 2010's normal sales show no price selection, mean residual -0.001); remove `Trivial` (`Overall Qual` alone R² 0.682 against 0.911 for a linear model, worse in 13 of 13 windows); map the text codes (CLEAN-12); keep the name. Applied: the city assessor as the actor (direct fit), the remodel year after the sale and the one before construction set missing, the three `Exterior 2nd` spellings mapped (225 rows), the outlier drop written as an exception to CLEAN-11 via CLEAN-1 (the third target-outlier drop; amendment proposed in the working copy's REVIEW.md), the `PID` drop measured (block prefix -0.0005 RMSE, SE 0.0005), stale numbers updated; the data change, so the container needs a rebuild. Priority 3: gap -, use case + (the codebook names the assessor's valuation of sold homes; direct fit), source + (De Cock's paper and codebook), shape +, risk - (non-market prices scored as the target until issue 7 is decided).

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
