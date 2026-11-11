---
unique_name: melbourne_housing_market
name: Melbourne Housing Market
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2017'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market
- https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot
v2_path: datasets/_dev/tabarena-v0pt2/melbourne_housing_market/dataset.py
source_row: 726
type_adapter_id: curation-record-v1
---

## Comments

Similar to GOV data, no predictive task connected so far.

Unclear which version to use, scraped data in many cases.

Otherwise okay and another price prediction task for some cases.

**Assessment (AI, 2026-10-07):** Valid as a sale-price regression over Domain.com.au's weekly auction sheets, split by time. Version: Melbourne_housing_FULL.csv (Jan 2016 to Mar 2018): its realestate.com.au attributes lower RMSE in log price from 0.211 (the LESS file's columns) to 0.183. These were looked up after the sale, but close to it from late 2016 on: `Bedroom2` matches the sheet's bedroom count in 98.9-100% of each test window, against 85.2% for the Apr-Sep 2016 sales looked up in April 2017. Only S/SP/SA prices are sales; PI and VB prices are bids (4.3% and 6.6% below a sale-price model), dropped. dansbecker/melbourne-housing-snapshot (record melbourne_housing_snapshot) is a September 2017 subset of the full file. The Airbnb links belong to record melbourne_airbnb_open_data.

Related work, not a source: Melbourne Airbnb listings (https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data, from Inside Airbnb, https://insideairbnb.com/).

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Sizeable temporal, spatial house-price regression with mixed features; useful but adds to an already well-covered house-price domain.

**Assessment (AI, 2026-10-20):** review panel (full tier): ship after changes. Sale-price regression of the Melbourne properties that sell, predicted before the auction (USE-3 wording fixed in the definition); 21,266 sales, 9 windows of three weekly sheets. Passed-in and vendor-bid prices are bids (-4.1% and -6.5% against a sale model, sales +0.3%), so only sales stay (USE-5, LEAK-22 hold). LightGBM skill 0.840 over the dummy on 5 of 5 probed splits, best single feature 0.426. Known risk: post-sale lookup of six attributes, measured small: Bedroom2 equals the sheet's Rooms in 98.9-100% of each test window (85.2% in Apr-Sep 2016), the September 2017 snapshot fixes all six for the 2,728 test rows up to 23 Sep 2017, the other five have no pre-sale reference, and blanking the 495 mismatched 2016 sales moves the RMSE by -0.0005 to +0.0003 over 3 seeds, inside the run-to-run spread of 0.0007; the coordinates come from the same lookup. Kept under a `Potential leak, kept on purpose:` note; the panel recommends fit `approximate` like house_sales, the curator decides (REVIEW issue 3); year 2018 under PROV-9's growing-source clause (issue 9). Repairs: 86 impossible BuildingArea values set missing, one Distance per suburb, two suburb lookups filled. Priority 2: gap -, use case -, source +, shape +, risk - (no thin domain, problem type or regime; the use case is the curation's, not the source's, and the fit is in question; documented Kaggle scrape with a data card; the post-sale lookup is an open leak issue).

CC (2026-10-21, Lennart): Blank the attributes looked up after the sale for the rows before the lookup (the smallest fix, LEAK-7), rather than keep them because removing them changes no score; stay with direct fit; measure the newest months for a recording shortfall and take a gap only if it shows selection.

**Assessment (AI, 2026-10-21):** The uploader looked the six attributes up for all sales up to the sheet of 8 April 2017 at once, by 10 April 2017 (Kaggle thread 30748), up to 15 months after the sale; later sales were looked up by weekly runs. The six attributes of these 7,578 sales (6,065 had them) are now blank, so missingness follows the date. Bedroom2 equals Rooms in 84-88% of each month of April-September 2016 and 99.2-100% of each month from November 2016. Cost: RMSE +0.0011 to +0.0016 over 3 seeds (0.1813 to 0.1826, 6-7 of 9 windows worse). Fit stays `direct`. Recording shortfall: every weekly sheet of the full file from August 2017 to 17 March 2018 holds as many sales as the same sheet of the companion file read up to October 2018 (558 of 558 on 17 March 2018); March 2018 holds 1,121 sales in three sheets against 1,174 in the same sheets of 2017; the newest window's mean residual is +0.009 against -0.013 to +0.022 in the others. No shortfall, no gap. Dataset check: 0 errors, 0 warnings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Kaggle dataset without a task or metric; regression fallback rmse (on the log target, close to RMSLE).

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a sale price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

CC (2026-10-22, Lennart): verdict ship. Issue 9: use 2017.

**Assessment (AI, 2026-10-22):** `year` is 2017, the Kaggle upload's first version; PROV-9 now says a Kaggle upload that grew over its versions is one publication and takes its first version's year (the growing-source clause covers registers and archives we snapshot). The BibTeX keeps the version we use (2018). REVIEW.md removed (nothing left open). Not built yet.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nsw_property_sales` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Lennart): REVIEW issue 10 (keep the nine windows or add July 2017), as implemented (A): the nine windows of three weekly sheets, 12 August 2017 to 17 March 2018, stay; 15-29 July 2017 is not added. The windows walk back from the newest because nine is the count of splits an IID task of this size gets and, further back, the train sides hold mostly the inner-suburbs-only file before 27 May 2017.

CC (2026-11-11, Lennart): the declared horizon (three weekly sheets, no gap, windows starting 2018-03-03, 2018-02-10, 2018-01-20, 2017-11-25, 2017-11-04, 2017-10-14, 2017-09-23, 2017-09-03 and 2017-08-12) is checked, as a Melbourne auction campaign runs about four weeks, so a price estimated during it looks one to four sheets ahead, and three sheets give nine windows that each train on at least 55.3% of the sales.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=3, unit="unique", n_windows=9, min_train_fraction=0.5`); test 1,119, 1,069, 93, 1,526, 1,033, 1,550, 868, 1,140 and 1,115 sales, train 20,147, 19,078, 18,985, 17,459, 16,426, 14,876, 14,008, 12,868 and 11,753 (94.7% to 55.3% of 21,266). The sales before 27 May 2017 (8,616, 40.5% of the rows) make up 79.2% of the train side of the tenth window (15-29 July 2017, 51.2%) and all of it from the window of 27 May to 17 June 2017 on (40.5%); the windows from 6-20 May 2017 back test the inner suburbs only, and three-sheet windows reach 30% of the rows back to 4-18 March 2017 (31.1%). `splits_comment` gives the campaign (Nelson Alexander) as the length's reason and these two reasons for walking back, without the "eight months of eligible history" of the issue's notes; `task_summary.split` and the decision table on the window length name the campaign. The issue's sentence that no dataset tests more windows than the IID folds is false: rain_in_australia tests 26 windows against 9 IID folds. `dataset check`: 0 errors, 0 warnings (README not regenerated).
