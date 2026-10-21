---
unique_name: house_sales
name: house_sales
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: GOV Website
year: '2016'
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

## Reference

https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
