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
collections:
- TabArena Reject
- TabSTAR
original_source: GOV Website
year: '2015'
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

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `view`, `condition`, `grade`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3).

## Reference

https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
