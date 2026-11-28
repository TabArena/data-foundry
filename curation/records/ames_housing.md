---
unique_name: ames_housing
name: Ames Housing (De Cock 2011)
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- Dated Event Log
original_source: Other
year: '2011'
collection_period: Jan 2006 - Jul 2010
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

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes. For the curator (Review issues 7, 4, 3, 9, 10): drop the 82 Family, Alloca and AdjLand sales by USE-5 (34 of them scored; mean scored RMSE -0.0051, SE 0.0029, lower in 8 of 13 windows); keep no gap as an exception to SPLIT-10 that rests on the mechanism (the short June 2010's normal sales show no price selection, mean residual -0.001); remove `Trivial` (`Overall Qual` alone R² 0.682 against 0.911 for a linear model, worse in 13 of 13 windows); map the text codes (CLEAN-12); keep the name. Applied: the city assessor as the actor (direct fit), the remodel year after the sale and the one before construction set missing, the three `Exterior 2nd` spellings mapped (225 rows), the outlier drop written as an exception to CLEAN-11 via CLEAN-1 (the third target-outlier drop; amendment proposed in the working copy's REVIEW.md), the `PID` drop measured (block prefix -0.0005 RMSE, SE 0.0005), stale numbers updated; the data change, so the container needs a rebuild. Priority 3: gap -, use case + (the codebook names the assessor's valuation of sold homes; direct fit), source + (De Cock's paper and codebook), shape +, risk - (non-market prices scored as the target until issue 7 is decided).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE between the logarithm of the predicted and the observed sale price (https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/overview/evaluation).

CC (2026-10-26, Lennart): issue 7: drop the allocation and adjoining-land sales, "as we know from the metadata what data to use to build the real task" (USE-5). The family sales wait for a consistency check (house_sales keeps its related-party sales, CC 2026-10-22).

CC (2026-10-26, Lennart): issue 9: map the text codes of the 43 categorical columns to the documentation's labels (CLEAN-12).

CC (2026-10-26, Lennart): issue 3: remove the `Trivial` marker (TP-4: `Overall Qual` alone R² 0.682 against 0.911 for a linear model).

**Exception to SPLIT-10 (2026-10-26, Lennart):** no gap between training and test windows. The only visible recording shortfall is the extract's last month (June 2010, 82 sales against 97-112 in earlier Junes), and its 73 normal sales show no price selection (mean residual -0.001); sales are dated by month, so the smallest possible gap is a whole month, longer than the delay. Serves P4: the windows train on every recorded sale before them, as a valuation model refit each month on all earlier sales would ("on such small data we could refit easily per month").

**Assessment (AI, 2026-10-26):** the decisions of 2026-10-26 applied: the 36 allocation and adjoining-land sales dropped (2,883 sales; 17 had been test rows; the 46 family sales wait for issue 7), the SPLIT-10 exception written, 266 codes of 43 columns written as DataDocumentation.txt labels (five codes the file spells unlike the documentation matched by hand: `A (agr)`, `C (all)`, `I (all)`, `NAmes`, `2fmCon`/`Duplex`/`Twnhs`; the documentation's typos corrected), the `Trivial` marker removed. `dataset check` clean; task probes on the 13 windows: linear R² 0.912 (RMSE 0.118), LightGBM 0.905, `Overall Qual` alone 0.682, no flag. The rename (issue 10) waits for the consistency check.

CC (2026-10-26, Lennart): issue 7: "do (c)": drop the 46 family sales as well (all 82 non-market sales go), and reopen house_sales issue 8 to drop its related-party sales (code 51) the same way.

CC (2026-10-26, Lennart): issue 10: "we could also just copy forward a new record, make the old one as duplicate and have the new name": the definition moves to this record, ames_housing; house_prices_nominal keeps its name and its links as the `Duplicate`.

CC (2026-10-26, Lennart): the declared metric, RMSE on the log price (the Kaggle competition's), is checked as declared.

**Assessment (AI, 2026-10-26):** folder moved to `datasets/_dev/tabarena-v0pt2/ames_housing/` (class `AmesHousing`; the raw file copied to `local-data-warehouse/ames_housing/`, same SHA-256). All 82 non-market sales dropped: 2,837 sales, 13 windows of 46-187 test sales. `dataset check` clean; task probes: linear R² 0.917 (RMSE 0.114), LightGBM 0.908, `Overall Qual` alone 0.691, no flag. No open issue is left, so the folder's REVIEW.md is removed; the record keeps `WIP (DF)` until the curator's ship verdict.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels): 12 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Lot Shape`, `Utilities`, `Land Slope`, `Exter Qual`, `Exter Cond`, `Heating QC`, `Kitchen Qual`, `Functional`, `Garage Qual`, `Garage Cond`, `Paved Drive`, `Pool QC` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `Garage Qual`, `Garage Cond`, `Pool QC` (CLEAN-10); left unordered: `Bsmt Qual` (a level outside the scale is a state of its own); `Bsmt Cond` (a level outside the scale is a state of its own); `Bsmt Exposure` (a level outside the scale is a state of its own); `BsmtFin Type 1` (a level outside the scale is a state of its own); `BsmtFin Type 2` (a level outside the scale is a state of its own); `Electrical` (a level outside the scale is a state of its own); `Fireplace Qu` (a level outside the scale is a state of its own); `Garage Finish` (a level outside the scale is a state of its own); `Fence` (a partial order); ordinal scales shipped as numbers, left as numbers for the curator's review: `Overall Qual`, `Overall Cond`.

CC (2026-10-31, Lennart): decided in the dtype review of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 ordinal scales shipped as numbers are ordered categories (point 3); 8 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `cook_county_residential_sales` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 2 coded columns carry their words.

CC (2026-11-04, Lennart): SPLIT-10 is amended (on lt_vehicle_loan_default_prediction): no gap is needed where the collection covers the label's delay and the measurements show no shortcut and no selection at the release end. The no-gap call here is now an application of the rule, not an exception; the line above stays as its history.

CC (2026-11-17, Andrej): the declared split (temporal on `Month Sold`, windows of 2 months, windows while training keeps 50% of the rows (13 in the build), no gap) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-26, Lennart): accepted `splits_dimensions_off_protocol` (SPLIT-15) after the rebuild of 2026-11-26: thirteen windows against SPLIT-33's 30; a fourteenth would train on 47% of the sales.

CC (2026-11-27, Andrej): Review issue 1: Option A, ship the transaction price ("Ship the transaction price: reword the question, use case and predicted fields"). The question, use case, row and predicted fields now say the task prices a recorded sale given its type and condition; data, features and split unchanged. The sentence on the sales-ratio standard is struck from the notes and the decision table, since it is wrong in both directions.

CC (2026-11-27, Andrej): Review issue 2: as implemented (B), the 12 adjoining-land sales stay dropped; the notes no longer cite the standard for the drop, which rests on the curator's call.

CC (2026-11-27, Andrej): Review issue 3: as implemented (A), 13 windows; the below-target warning is accepted with the numbers (the five further windows train on 33.6% to 46.8% of the sales and the exception stays untaken).

CC (2026-11-27, Andrej): ship as defined (review of 2026-11-27).

**Assessment (AI, 2026-11-27):** applied; `dataset check` 0 errors, 2,837 rows and the 13 windows unchanged, `splits_below_target` accepted in the definition. Reworded: question, use case, row, predicted, the prediction-point note, the sale-filter note and its decision-table entry.

## Review

**Outcome:** added. Decided on 2026-11-27: ship the price of a recorded sale given its type and condition (issue 1, A, words only), keep the 12 adjoining-land sales dropped (issue 2, B) and keep 13 windows with the warning accepted (issue 3, A). The sale records hold up on every test designed to break them and no leak was found by any route.

**Main points:** Nothing open.

**Issues for Andrej:**

1. **Which prediction point ships: a sale that has happened, or a house being valued?**

   * **Problem:**
     - The prediction-point note says "a house sells, and a valuation model predicts its price", while the use case says the assessor "estimates what each house would sell for"; an assessor valuing an unsold house holds neither the sale's type nor its condition, and a model pricing a recorded sale holds both.
     - The sale's condition is already the row filter, since the 82 non-market sales are dropped by it, so the same field both screens the rows and feeds the model.
     - The standard the definition cites for that screening says the opposite of the line drawn: it forbids forced sales for model calibration, which are kept, and forbids excluding adjoining-owner sales for that reason alone, which are dropped.
   * **Effect on the task:** Under the first reading the benchmark measures the price of a recorded transaction, discount and all; under the second it measures market value, and the distressed sales and their condition field do not belong in it. A participant cannot tell which is scored.
   * **Experiments:**

     | Measure (LightGBM, 13 windows) | Value |
     |---|---|
     | Cost of dropping both transaction fields | +0.00504 RMSE (SE 0.00104), worse in 12 of 13 windows |
     | Cost of dropping the sale's condition alone | +0.00409 (SE 0.00108), worse in 11 of 13 |
     | Bias on the distressed sales, with the fields | -0.070 |
     | Bias on the distressed sales, without them | -0.126 |
     | Share of the scored squared error held by the 94 distressed sales | 31.6% |

     The suspicion that the condition is assigned from the price was tested as the sibling dataset's was, on out-of-fold residuals with both fields withheld:

     | Group | Rows | Mean residual | Above +0.3 | Below -0.3 |
     |---|---|---|---|---|
     | Normal | 2,405 | +0.009 | 0.8% | 0.5% |
     | Abnormal | 190 | -0.099 | 3.2% | 12.6% |
     | Partial | 242 | +0.021 | 0.4% | 1.2% |
     | the sibling's dropped group, for comparison | 357 | — | 0% | 29% |

     The distressed sales miss on both sides, where the sibling's dropped group missed only on one, so the one-sided signature that convicted it is absent here.
   * **Consistency:** house_sales, decided by you a month ago, is the controlling sibling: it keeps the sales flagged as not at market value, ships the condition as a feature, and drops only the codes that are the appraiser's judgment formed with the price in view. As shipped, this dataset matches it in every respect but the use-case sentence.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship the transaction price: reword the question, use case and predicted fields | words only; data, features and split unchanged | matches what already ships and follows the sibling with no departure to argue | the actor is a party to a recorded sale, not an assessor valuing an unsold house |
     | B | Ship the market value: drop the two fields and the 190 distressed sales, keep the assessor wording | the only reading the cited standard supports | a genuine mass-appraisal task | a task change and its own pull request; costs 0.00504 RMSE and 94 scored rows; the split's leaf moves to the fill-in reading, against the forward windows your blind walk confirmed; departs from house_sales, which would have to be reopened |
     | C | Keep both wordings (implemented) | nothing changes | no work | a participant cannot tell which task is scored, and the cited standard supports neither line as drawn |

   * **Recommendation:** A, with the sentence about the standard struck whichever way you decide, since it is wrong in both directions. **Decision:** A, B or C?

   **Notes for the AI:** under B the consistency check is owed against house_sales (2026-10-22 and 10-26), and the departure needs the fact that sets this case apart or house_sales reopened. The two do not share a mechanism: there the codes are county warnings set after recording, here the condition is in the source's own file. Cite house_sales for its measured gain and its one-sided test, not for the mechanism (house_sales re-audit, 2026-11-26).

   **Andrej (2026-11-27, change):** Option A: Ship the transaction price: reword the question, use case and predicted fields.

   **Resolved (2026-11-27, Andrej):** A. The question, use case, row and predicted fields describe the price of a recorded sale given its type and condition; the prediction-point note says so too, and the sentence on the cited standard is struck. Data, features and split are unchanged; `dataset check` 0 errors.

2. **Bring back the 12 adjoining-owner sales?**

   * **Problem:**
     - They were dropped as not this house's market value, citing a standard whose one clause on them says they "should not be excluded solely because the buyer owns adjoining property".
     - Conditional on the features they sell above the model, not below, so the data does not support the stated reason.
     - The two other dropped groups are supported by the same standard and stay either way.
   * **Effect on the task:** 12 rows, 2 of them scored. Negligible in score; it is a consistency point.
   * **Experiments:**

     | Group | Rows | Mean residual | Below -0.3 |
     |---|---|---|---|
     | Adjoining land | 12 | +0.057 | 0.0% |
     | Normal | 2,405 | +0.009 | 0.5% |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Reinstate the 12, with their condition recorded in the feature | adds 12 rows, 2 scored | follows the cited standard and the measurement; consistent with the sibling | adds rows carrying a second arm's-length doubt; pointless if issue 1 goes B |
     | B | Keep them dropped (implemented) | nothing changes | simplest; correct if issue 1 goes B | its only stated authority says the opposite, and the data show no discount |

   * **Recommendation:** A if issue 1 goes A; B if issue 1 goes B. **Decision:** A or B?

   **Andrej (2026-11-27, ok):** As implemented (B).

   **Resolved (2026-11-27, Andrej):** B, the 12 adjoining-land sales stay dropped; the drop is worded as the curator's call, with no claim that the standard supports it.

3. **Take the training-floor exception to test 2007 as well, or keep 13 windows?**

   * **Problem:**
     - The check warns that 13 windows stand against the 30 an equivalent random split would get, and the definition accepts nothing, although the splits comment already gives the argument the warning asks for.
     - Five further windows sit just under the training floor, inside the exception only you can take, and they are the only access to 2007 and to the turn of the market.
     - Those five are measurably a different regime, so the shipped split never tests the conditions a model deployed in 2008 would have met.
   * **Effect on the task:** Today every scored sale falls in 2008 to 2010. With the five, the score also covers the top of the market and its turn.
   * **Experiments:**

     | Windows | Training share | Test sales | LightGBM RMSE |
     |---|---|---|---|
     | the shipped thirteen | 0.501 to 0.944 | 46 to 187 | 0.119 mean |
     | the five further ones | 0.336 to 0.468 | 53 to 180 | 0.146 mean |
     | of those, January-February 2008 alone | 0.449 | 85 | 0.236 |

   * **Consistency:** The floor's amendment names exactly this case, windows that add years, seasons or events the newest ones lack. Only a person may take the exception.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep 13 windows and accept the warning (implemented) | one acceptance entry, no prose, no re-split | every window clears both floors with no exception owed | 13 against a target of 30; no 2007 sale is ever scored |
     | B | Go to 18 windows by taking the exception | adds the five windows down to a third of the rows in training | the only access to 2007 and the turn; moves the count toward the target; the rule's amendment names this case | five windows train on a third to a half of the data, unlike any deployment; needs your line on the record and an accepted second warning |

   * **Recommendation:** A is fully compliant and is what the split auditor recommends; the mediator leans B, because the preference for other years is explicit and 2008 is the regime a deployed model had to handle. A ships unless you write the line. **Decision:** A or B?

   **Andrej (2026-11-27, ok):** As implemented (A).

   **Resolved (2026-11-27, Andrej):** A, 13 windows; `splits_below_target` is accepted in the definition with the numbers of the five further windows (33.6% to 46.8% training share) and the date.

**Review panel:** ship after changes (mediator, focused tier: claim auditor, column auditor, split auditor, task gamer).
Claims: 29 tested, 16 hold, 11 refuted on wording and counts, 2 untested. Columns: no post-outcome value; two garage
columns apply the absent-state rule backwards, which the fix measures free. Split: right with notes; the blind tree
walk reaches the leaf that ships. Task gamer: could not game it, and found the outlier filter is defined by the label
although its effect measures +0.00009. Agreed: no leak by any route. Disputed: which use case ships (issue 1).

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
