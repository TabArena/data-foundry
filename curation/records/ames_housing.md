---
unique_name: ames_housing
name: Ames Housing (De Cock 2011)
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
original_source: Other
year: '2011'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1080/10691898.2011.11889627
- https://jse.amstat.org/v19n3/decock/AmesHousing.txt
- https://jse.amstat.org/v19n3/decock/DataDocumentation.txt
v2_path: datasets/_dev/tabarena-v0pt2/ames_housing/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Copied forward from house_prices_nominal on 2026-10-26 (CC 2026-10-26, Lennart, below): this record is De Cock's full Ames file (2,930 sales, 2006-2010) that the working copy's definition ships; house_prices_nominal, the Kaggle competition's 1,460-row half (OpenML 42165, in TabSTAR), is now its `Duplicate`. The comments below are house_prices_nominal's, copied as they were.

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

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE between the logarithm of the predicted and the observed sale price (https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/overview/evaluation).

CC (2026-10-26, Lennart): issue 7: drop the allocation and adjoining-land sales, "as we know from the metadata what data to use to build the real task" (USE-5). The family sales wait for the consistency check on the review page (house_sales keeps its related-party sales, CC 2026-10-22).

CC (2026-10-26, Lennart): issue 9: map the text codes of the 43 categorical columns to the documentation's labels (CLEAN-12).

CC (2026-10-26, Lennart): issue 3: remove the `Trivial` marker (TP-4: `Overall Qual` alone R² 0.682 against 0.911 for a linear model).

**Exception to SPLIT-10 (2026-10-26, Lennart):** no gap between training and test windows. The only visible recording shortfall is the extract's last month (June 2010, 82 sales against 97-112 in earlier Junes), and its 73 normal sales show no price selection (mean residual -0.001); sales are dated by month, so the smallest possible gap is a whole month, longer than the delay. Serves P4: the windows train on every recorded sale before them, as a valuation model refit each month on all earlier sales would ("on such small data we could refit easily per month").

**Assessment (AI, 2026-10-26):** the marks of 2026-10-26 applied: the 36 allocation and adjoining-land sales dropped (2,883 sales; 17 had been test rows; the 46 family sales wait for issue 7), the SPLIT-10 exception written, 266 codes of 43 columns written as DataDocumentation.txt labels (five codes the file spells unlike the documentation matched by hand: `A (agr)`, `C (all)`, `I (all)`, `NAmes`, `2fmCon`/`Duplex`/`Twnhs`; the documentation's typos corrected), the `Trivial` marker removed. `dataset check` clean; task probes on the 13 windows: linear R² 0.912 (RMSE 0.118), LightGBM 0.905, `Overall Qual` alone 0.682, no flag. The rename (issue 10) waits for the consistency check.

CC (2026-10-26, Lennart): issue 7: "do (c)": drop the 46 family sales as well (all 82 non-market sales go), and reopen house_sales issue 8 to drop its related-party sales (code 51) the same way.

CC (2026-10-26, Lennart): issue 10: "we could also just copy forward a new record, make the old one as duplicate and have the new name": the definition moves to this record, ames_housing; house_prices_nominal keeps its name and its links as the `Duplicate`.

CC (2026-10-26, Lennart): the declared metric, RMSE on the log price (the Kaggle competition's), is checked as declared.

**Assessment (AI, 2026-10-26):** folder moved to `datasets/_dev/tabarena-v0pt2/ames_housing/` (class `AmesHousing`; the raw file copied to `local-data-warehouse/ames_housing/`, same SHA-256). All 82 non-market sales dropped: 2,837 sales, 13 windows of 46-187 test sales. `dataset check` clean; task probes: linear R² 0.917 (RMSE 0.114), LightGBM 0.908, `Overall Qual` alone 0.691, no flag. No open issue is left, so the folder's REVIEW.md is removed; the record keeps `WIP (DF)` until the curator's ship verdict.

CC (2026-10-26, Lennart): verdict ship.

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
