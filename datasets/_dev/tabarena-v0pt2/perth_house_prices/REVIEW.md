# perth_house_prices

**Outcome:** added. A regression of the log sale price of Perth houses scraped from house.speakingsame.com, temporal
with nine one-month test windows (April to December 2020) and no gap. The AI recommends shipping it, with the
concerns below.

**Main points:** The upload holds no sale above $2.44M (a capped target). In 2019-2020 the house records are often
older than the sale.

**Record judgment:** valid with concerns. Provenance is traceable and the data is unique. The concerns change what the
task measures, but none is a leak: the scrape's sampling (issue 3), an undocumented price cap (issue 1), test-period
records older than the sale (issue 2) and pre-build sales (issue 4).

**Issues for Lennart:**

1. **The target is capped at $2,440,000 (new, from the verifier; reproduced).**
   - Evidence:
     - No sale in the file is above $2,440,000, and the yearly maximum is $2.40-2.44M in every year 2011-2020.
     - The counts fall smoothly to 46 sales between $2.3M and $2.4M (45 after cleaning) and 11 between $2.4M and $2.44M,
       then stop.
     - The site lists dearer sales: 17 McNeil Street, Peppermint Grove, "Sold $5,200,000 in Jun 2013" (archived
       2022-08-10).
     - heptix/perth-property-prices has 75 of 5,072 houses sold in 2015-2020 (1.48%) above the cap. Among the 2018-2020
       sales of all types it has 40% of Peppermint Grove's 15 and 48% of Dalkeith's 25 above it.
     - Dalkeith's median here is $2,039,000 (55% of its sales at $2M or more). Peppermint Grove has 41 rows and none
       after March 2018.
     - The 7 suburbs with 13-55% of their sales at $2M or more hold 45 of the 4,132 test rows, and 29 test rows are at
       $2M or more.
   - Implemented: keep, with an `Anomaly:` bullet and a decision table. This source cannot give the missing sales back.
   - Question: is a task "price of a sale up to about $2.44M" acceptable? §D.6 asks to document a capped target;
     cirrhosis is a precedent for a recorded selection.

2. **In the test period the site's record of a house is often older than the sale (new, from the verifier; reproduced).**
   - Evidence: of the 1,824 sales shared with heptix's sold listings, bedrooms or bathrooms differ in:
     - 0.7% of 2007-2016;
     - 2.8% of 2017-2018;
     - 12.1% of 2019;
     - 27.0% of 2020.
   - The file nearly always has fewer: in 2020, fewer in 22.9% and more in 4.3%. The step comes in mid-2019: 5.7% and
     2.3% in 2019Q1-Q2, then 15%, 14%, 29%, 25%, 21%, 19%.
   - A missing GARAGE marks these rows: among the shared 2019-2020 sales, 45.7% of those without a car count are stale,
     against 13.9% of the others.
   - Not a leak, unlike King County. LightGBM on the shipped windows scores the 349 shared test rows at RMSE 0.138 with
     the file's values and 0.126 with the sold listing's. On the 90 rows that differ: 0.154 against 0.123, with the
     file's values under-predicting by 0.045.
   - Implemented: keep, with an `Anomaly:` bullet. This replaces my earlier "Changes to a house after its sale ...
     cannot be seen in the file", which the comparison contradicts.
   - Question: is a test period in this stale regime acceptable?
   - Alternative, not recommended: end the data before July 2019. This loses 7,978 rows, and the test windows would move
     to late 2018 to mid-2019. The 9 x 3-month windows of issue 6 would put their 3 oldest windows before the step.

3. **The scrape's sampling shapes the training history.**
   - Each property appears once, with its latest sale (discussion 383033).
   - Each suburb holds only its newest sales: 1-231 rows, mean 103. Busy suburbs start in 2018-2020 (Butler Sep 2018,
     Ellenbrook Jul 2019, Baldivis May 2020); quiet ones reach back to 1988.
   - So the years before 2013 hold 2,263 sales, mostly of quiet suburbs and of houses not resold. Baldivis has no
     training rows for the April 2020 window.
   - Implemented: keep all rows.
   - Alternative: keep sales from 2013 on only (mean RMSE 0.1612 → 0.1607).

4. **The build-year rule removes only part of the land and off-the-plan sales; all of them are training rows.**
   - 563 sales dated before the build year are dropped. Cross-fitted LightGBM prices them 0.23 log units too high on
     average.
   - The 140 sales in the build year stay, although 9-13% of them are priced more than 0.5 log units too high (two
     runs), against 1.2-1.3% of older houses.
   - Sales without a build year before 2005 (51 rows) have a mean residual of -0.21 to -0.22, with 29-33% below -0.5.
   - The test period shows no excess: in 2020, 0.2-0.8% of each group is below -0.5.
   - Dropping the 563 changes test RMSE by 0.0004. Alternative: keep them.

5. **ADDRESS is kept as a string feature.**
   - Its unit numbers (1,060 rows, median price $404,000 against $540,000) and lettered lots (2,615) are the only trace
     of the property type, which the site shows and the upload dropped.
   - A derived unit flag lowers LightGBM's mean RMSE from 0.161 to 0.158 (lower in 7 of 9 windows).
   - The probe's text encoding gains nothing: RF R² 0.849 with the text, 0.865 without; LightGBM 0.863 and 0.865.
     Tokenising drops the "/".
   - Kept as text, as melbourne_housing_market and california_house_prices_2020 do.
   - Alternatives: a `UNIT` flag ("reconstruct destroyed meaning", patterns §D.12), with or without the text; or drop
     ADDRESS.
   - Not tested: how `tabarena_default`'s text embedding uses the column.

6. **Window length.**
   - Implemented: 9 x 1 month, April-December 2020, 284-628 sales per window, oldest train share 88%. All windows fall
     in 2020 and in the stale regime of issue 2.
   - Alternatives: 9 x 2 months, July 2019 to December 2020 (658-1,197 sales, train share from 76%); or 9 x 3 months,
     October 2018 to December 2020 (974-1,619, from 64%).

7. **No planning gap.**
   - Many sales reach the site within days: an archived Mount Lawley page of 14 April 2021 lists four sales of April
     2021 among its 10 newest. Still, a month after its end, December 2020 held about 80% of its usual share of
     November's count.
   - Implemented: no gap, as house_sales and house_prices_nominal.
   - Alternative: a one-month gap, as zillow_prize (LightGBM mean RMSE 0.159 → 0.162).

8. **December 2020 is kept although it is short.**
   - 412 sales; December/November is 0.71 against 0.83-1.04 in 2013-2019.
   - Its prices relative to each suburb's median are not lower: +0.048, against +0.027 in November and +0.023 in
     October.
   - Alternative: drop the month, as house_sales dropped its cut-short May 2015.

9. **Implausible and probably non-market rows are kept.**
   - 52 sales since 2012 are below $120,000.
   - 19 houses of 2-4 bedrooms have 1-40 m² of floor area; one house of 95 m² has 16 bathrooms.
   - Strata units often carry the land area of the whole complex.
   - The file has no sale type. A price floor of our own would filter on the target.

10. **The download is not pinned to a Kaggle version.** `kaggle datasets download syuzai/perth-house-prices/1`
    returns 404. The single version reproduces the sha256 today (the verifier re-downloaded it).

11. **Licence (noted only).** CC BY-NC-SA 4.0; the terms of house.speakingsame.com are not stated.

12. **Framework, not patched.** `meta_time_horizon_mismatch` fires for month-start dates in one-month windows. The check
    could measure a window from its start to the next window's start.

14. **Backlog note.** heptix/perth-property-prices (42,958 sales of 2006-2024, CC BY-SA 4.0, no stated source) has
    property type, agency, exact dates and no price cap. It has no floor area or build year. It is a separate candidate.
