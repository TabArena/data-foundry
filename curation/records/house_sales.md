---
unique_name: house_sales
name: house_sales
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
- 'Features: Read Later'
- Dated Event Log
collections:
- TabArena Reject
- TabSTAR
original_source: GOV Website
year: '2015'
collection_period: May 2014 - May 2015
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
- https://www.openml.org/d/42731
v2_path: datasets/_dev/tabarena-v0pt2/house_sales/dataset.py
source_row: 721
type_adapter_id: curation-record-v1
---

## Comments

CC: "Time split required. Also spatial data. Time impact not ignorable as collection and prediction was not at one time point"

Feature descriptions: https://www.kaggle.com/datasets/harlfoxem/housesalesprediction/discussion/207885

**Assessment (AI, 2026-10-07):** Provenance traced: the rows are King County Department of Assessments sales (21,386 of 21,613 match a recorded sale on parcel, date and price), first distributed in 2015 as `kc_house_data` with the University of Washington's Coursera ML Specialization; the Kaggle CSV is a cell-for-cell copy. The house features are the assessor's record as of 18-19 July 2015, not of each sale: for 2,151 rows the record changed after the sale, mostly upward, which flatters models (LightGBM RMSE on those rows 0.156 against 0.208 with the record at the sale). The v2 definition rebuilds each sale's record from the county's change log and drops May 2015, which the extract cut short.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Well-known house-price regression with its post-sale feature leak fixed; temporal split, spatial features, direct valuation fit.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes. Applied: the 1,061 sales the county flags as not at market value (warnings 15, 46, 60, 51, 23, 13) dropped from the county's sales extract (USE-5); the lot size rebuilt from the `LandFootage` record (LEAK-10); a one-week gap for the recording delay (SPLIT-10); the July-2015 view, waterfront and neighbours' areas kept with a `Potential leak, kept on purpose:` note and the fit set to approximate (USE-8); 5 placeholder living areas set to missing; the use case reworded to the assessor's record on the sale day; the 2015 course release and the county cited (PROV-10). Open: the borderline warning codes, `yr_renovated` 0 as missing, and the house-price family's fit label and window length. Priority 3: gap -, use case -, source +, shape +, risk - (no thin domain, problem type or regime; the use case is the curation's and the fit approximate; King County's assessor records; 19,906 sales, temporal, mixed feature types; no known risk, the open issues are scope and encoding).

CC (2026-10-21, Lennart): Stay with direct fit if the task (without leakage) would be a direct fit, and only move to approximate if we had to change a lot to avoid the leak; keep the horizons as they are, no family-wide window.

**Assessment (AI, 2026-10-21):** fit set back to `direct`; `fit_reason` names the remnant kept from July 2015 (view, waterfront and the neighbours' areas changed after the sale for about 145 rows; masking them: RMSE 0.2147 against 0.2132) and the 1,073 sales flagged as changed since the sale. Dataset check: 0 errors, 0 warnings.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: waterfront.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Neither the King County assessor extracts nor the Kaggle dataset card define a task metric; the Coursera course that first distributed kc_house_data used RSS/RMSE on raw price as a teaching exercise, not a benchmark definition. RMSE on the log price is the obvious choice for a price model.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a sale price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

CC (2026-10-22, Lennart): issue 9 as implemented: `yr_renovated` = 0 stays missing. Record field `year` takes the definition's value (2015).

**Exception to CLEAN-10 (2026-10-22, Lennart):** `yr_renovated` = 0 means "never renovated" and is set to missing instead of kept as a code; what sets it apart from bank_marketing and house_prices_nominal: a 0 in a year column reads as a year to a linear model, and after the as-of-sale rebuild missing has no other meaning in the column. Serves P7 (cleaning to the expert state: the column means what a model reads from it, CLEAN-1).

CC (2026-10-22, Lennart): issue 8: (c), keep the sales with codes known before the price and add an indicator; drop only the appraiser's judgment codes (46, 7, 8).

**Assessment (AI, 2026-10-22):** applied: 360 sales dropped (code 46: 357; code 8: 4), 20,607 rows; new categorical `sale_condition` (none 19,847; no market exposure 473; short sale 129; related party 85; other pre-price code 33; estate 32; bankruptcy or forced sale 8). Untuned LightGBM on the 9 windows, RMSE on log price all / unflagged / flagged: .1662 / .1613 / .2552, against .1682 / .1611 / .2875 when the old six codes are dropped; the short-sale mean residual moves from -0.23 to -0.04. dataset check: 0 errors, 0 warnings. New issue 10: codes 45, 5 and 1 (23 sales) whose price is not the house's alone.

CC (2026-10-22, Lennart): issue 10: drop the sales with warning 45, 5 or 1 (the recorded price is not this house's alone).

**Assessment (AI, 2026-10-22):** applied: 23 sales dropped (`PRICE_NOT_THE_HOUSE`), 20,584 rows and 20 features. dataset check: 0 errors, 0 warnings. REVIEW.md removed (nothing left open). Not built yet.

CC (2026-10-26, Lennart): on ames_housing issue 7 (option (c), "do (c)"): drop the related-party sales (warning 51) here too, as the family sales of ames_housing. This reopens issue 8 of 2026-10-22, option (c), which kept them with a `sale_condition` level; the other declared conditions stay as they were.

**Assessment (AI, 2026-10-26):** the 85 sales whose first `sale_condition` level was related party are dropped (91 sales carry warning 51; 6 were already dropped by another code): 20,499 sales. `sale_condition` loses its related-party level. `dataset check` clean; task probes (5 of 9 windows): LightGBM R² 0.894, no flag.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels): ordinal scales shipped as numbers, left as numbers for the curator's review: `view`, `condition`, `grade`.

CC (2026-10-31, Lennart): decided in the dtype review of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `cook_county_residential_sales` (TBD -> Yes, priority 3), `king_county_home_sales_1999_2025` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 2 coded columns carry their words; 1 scores are numbers (view).

CC (2026-11-17, Andrej): the declared split (temporal on `date`, windows of 3 weeks, up to 9 windows while training keeps 50% of the rows (9 in the build), gap 1 week) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

## Review

**Outcome:** added. Re-audited on 2026-11-26 against a King County extract six weeks newer than the one the
definition was written against: nothing changes in the data, the split or the verdict. The strongest result of the
round's reproducibility checks is this dataset's: `dataset check` regenerated its README byte-identical to the
committed page, from the newer extract, with the same 20,499 rows and the same container checksum. Every rebuilt
column is as of the sale, the split tree's leaf matches what ships, and the one-week gap does its job (median six days
from deed to recording, and under 1% of training rows recorded after their window starts). Four things need no
decision and are corrected in the text: three counts left over from the related-party drop of 2026-10-26 (20,607 sales
for 20,499, window sizes 649 to 1,534 for 643 to 1,518, and 9,498 test sales for 9,439); the definition's checksum
test, which compares three files where only the sales-warnings file guards the 2014-2015 records it names; and the
metric's reason, which does not say that the OpenML copy's task defaults to RMSE on the raw price. One issue is open.

**Main points:** Task gamer (blind, 2026-11-27): nothing gamed. Untuned LightGBM RMSLE 0.1666 (0.157 to 0.178 over 9 windows; a random column moves it by up to 0.004 per split); the last training sale of the same house (1.6% of test rows) does worse (0.1741), `sale_condition` adds 0.002 and is declared at sale, and the kept July-2015 neighbour sizes add 0.0007, inside noise (the known kept leak). Training on the last 120 days only scores worse (0.1733). One for you: whether the note on the sale-condition column says more than the files show about when
each code is set (1). This dataset is the precedent `ames_housing` cites, and it holds on measurement.

**Issues for Andrej:**

1. **Soften the claim that the sale-condition codes are declared by the parties?**

   * **Problem:**
     - The use case says the sale's condition is "declared by the parties", while the same note says the county sets its sale warnings after the deed is recorded.
     - The extract carries no timestamp or setter for any code, so when each one is set cannot be shown from the files.
     - The claim matters beyond this dataset, because `ames_housing` cites this one as the precedent for keeping a sale's condition as a feature.
   * **Effect on the task:** None on the data. The column is worth keeping on measurement; what is overstated is the reason given for its timing.
   * **Experiments:** shipped splits, untuned LightGBM, mean residual on the log price with and without the column.

     | Level | Scored rows | Without the column | With it |
     |---|---|---|---|
     | short sale | 57 | -0.218 | -0.028 |
     | no market exposure | 278 | -0.073 | +0.016 |
     | estate | 21 | -0.011 | +0.102 |
     | other pre-price code | 20 | -0.082 | +0.107 |

     Pooled RMSE on the log price is 0.1697 without the column and 0.1673 with it, better in 9 of 9 windows. Coded rows are 4% of the scored rows, and the two smallest levels hold about 20 rows each, so their signs are noise. The share coded does not fall toward the newest months, so there is no sign of codes arriving late.
   * **Consistency:** The precedent holds, but for a different reason than `ames_housing`'s review gives. Here the codes are county warnings set after recording with no timestamp; there the condition sits in the source's own file for the same sale. So a citation of this dataset should rest on the measured gain and on the one-sided test that justified dropping the appraiser's codes (none of that group above +0.3, 29% below -0.3), not on the two having the same mechanism.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the wording (implemented) | "declared by the parties" stays | the column's gain is measured | the note claims more than the files show |
     | B | Keep the column, soften the wording | the note says the codes are county sale warnings naming facts the parties know, and that when each was set is not in the extract | honest; no data change | one sentence |
     | C | Keep only the short-sale, bankruptcy and estate levels | drops the no-market-exposure level and the minor codes | the fewest doubtful codes | loses 471 rows' level and reopens a settled call |

   * **Recommendation:** B. The column earns its place on measurement, so only the account of its timing needs to change. **Decision:** A, B or C?

**Review panel:** ship (audit against the source, the newer extract and the recording dates; no separate mediator).
Claims: every count but three reproduces, and the three are left over from a drop applied on 2026-10-26. Columns:
every rebuilt column is as of the sale, and the one flagged code is already typed correctly. Split: the tree reaches
the leaf that ships, with nine windows on the target and every training side different. Agreed: nothing changes in
the data. Disputed: nothing.

## Reference

https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
